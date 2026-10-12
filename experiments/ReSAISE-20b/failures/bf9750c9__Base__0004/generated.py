import urllib.parse

# Whitelisted domains that may be used as return URLs.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "myapp.org",
    "trustedsite.net"
}

def construct_sso_redirect(sso_uri: str, user_identifier: str, redirect_link: str) -> str:
    """
    Build an SSO redirect URL that includes the user identifier and a safe return link.

    Parameters
    ----------
    sso_uri : str
        The base SSO endpoint URL.
    user_identifier : str
        Unique identifier for the authenticated user.
    redirect_link : str
        The URL to return to after SSO completes.

    Returns
    -------
    str
        Fully constructed, URL‑encoded SSO redirect URL.

    Raises
    ------
    ValueError
        If the domain of `redirect_link` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the redirect link domain.
    parsed_redirect = urllib.parse.urlparse(redirect_link)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_link must be a fully-qualified URL")

    # Normalize the domain to lower case for comparison.
    redirect_domain = parsed_redirect.netloc.lower()
    if redirect_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return domain '{redirect_domain}' is not allowed")

    # Build query parameters.
    params = {
        "user_id": user_identifier,
        "return_url": redirect_link
    }

    # Parse the base SSO URI to preserve any existing query parameters.
    parsed_sso = urllib.parse.urlparse(sso_uri)
    # Merge existing query params with new ones.
    existing_params = urllib.parse.parse_qs(parsed_sso.query)
    # Flatten the values (parse_qs returns lists).
    existing_params = {k: v[0] for k, v in existing_params.items()}
    merged_params = {**existing_params, **params}

    # Reconstruct the full URL.
    new_query = urllib.parse.urlencode(merged_params)
    sso_parts = parsed_sso._replace(query=new_query, fragment="")
    full_url = urllib.parse.urlunparse(sso_parts)

    return full_url