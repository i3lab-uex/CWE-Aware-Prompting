import urllib.parse

# Whitelist of domains that can be used as the return URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    "trusted.com",
}

def construct_sso_redirect(sso_uri: str, user_identifier: str, redirect_link: str) -> str:
    """
    Construct an SSO redirect URL.

    Parameters
    ----------
    sso_uri : str
        Base URI of the SSO endpoint (may already contain query parameters).
    user_identifier : str
        Unique identifier of the user.
    redirect_link : str
        URL to which the user should be redirected after authentication.

    Returns
    -------
    str
        Full SSO redirect URL containing the user ID and return link.

    Raises
    ------
    ValueError
        If the domain of ``redirect_link`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect link to validate its domain
    parsed_redirect = urllib.parse.urlparse(redirect_link)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_link must be a valid absolute URL")

    # Extract the domain (hostname) without port
    host = parsed_redirect.hostname.lower()
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return domain '{host}' is not allowed")

    # Build the query parameters
    new_params = {
        "user_id": user_identifier,
        "return_url": redirect_link,
    }

    # Parse the base SSO URI to preserve existing query parameters
    parsed_sso = urllib.parse.urlparse(sso_uri)
    existing_params = dict(urllib.parse.parse_qsl(parsed_sso.query, keep_blank_values=True))
    # Merge new params over existing ones
    merged_params = {**existing_params, **new_params}

    # Reconstruct the full URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_sso.scheme,
            parsed_sso.netloc,
            parsed_sso.path,
            parsed_sso.params,
            urllib.parse.urlencode(merged_params, doseq=True),
            parsed_sso.fragment,
        )
    )

    return final_url