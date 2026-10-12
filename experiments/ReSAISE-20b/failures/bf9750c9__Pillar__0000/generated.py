import urllib.parse

# Whitelisted domains for the return URL (example entries)
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    "trusted-domain.net",
}

def construct_sso_redirect(sso_uri: str, user_identifier: str, redirect_link: str) -> str:
    """
    Construct an SSO redirect URL that includes the user identifier and a
    return URL, after validating that the return domain is approved.

    Parameters
    ----------
    sso_uri : str
        Base SSO endpoint URL.
    user_identifier : str
        Unique identifier for the user.
    redirect_link : str
        URL to return to after successful authentication.

    Returns
    -------
    str
        Fully constructed SSO redirect URL.

    Raises
    ------
    ValueError
        If the domain of ``redirect_link`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect link to extract its domain
    parsed_redirect = urllib.parse.urlparse(redirect_link)
    # Normalise the netloc (remove port if present for domain comparison)
    redirect_domain = parsed_redirect.hostname
    if not redirect_domain:
        raise ValueError("Redirect link must contain a valid hostname")

    # Ensure the domain is in the whitelist
    if redirect_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Domain '{redirect_domain}' is not allowed for redirect links")

    # Prepare query parameters
    params = {
        "user": user_identifier,
        "redirect": redirect_link,  # The SSO provider will handle decoding
    }

    # Parse the base SSO URI to safely add/merge query parameters
    parsed_sso = urllib.parse.urlparse(sso_uri)
    # Merge existing query params if any
    existing_params = dict(urllib.parse.parse_qsl(parsed_sso.query))
    merged_params = {**existing_params, **params}
    new_query = urllib.parse.urlencode(merged_params)

    # Reconstruct the full URL
    sso_redirect = urllib.parse.urlunparse(
        (
            parsed_sso.scheme,
            parsed_sso.netloc,
            parsed_sso.path,
            parsed_sso.params,
            new_query,
            parsed_sso.fragment,
        )
    )

    return sso_redirect