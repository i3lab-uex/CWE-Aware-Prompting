import urllib.parse

# Whitelist of allowed return domains (example)
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "myapp.org",
    "trusted.co.uk",
}

def create_sso_url(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        Base URL of the SSO provider.
    uid : str
        Unique identifier for the user.
    redirect_url : str
        URL to return to after authentication.

    Returns
    -------
    str
        Full SSO redirect URL ready for the client to follow.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect URL to inspect its domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_url must be a fully qualified URL")

    # Normalise domain: lower‑case and strip port
    host = parsed_redirect.netloc.split(":")[0].lower()

    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return domain '{host}' is not allowed")

    # Build query parameters
    query_params = {
        "uid": uid,
        "redirect_url": redirect_url,  # will be URL‑encoded by urlencode
    }

    # Parse the auth endpoint to merge existing query parameters if any
    parsed_auth = urllib.parse.urlparse(auth_endpoint)
    auth_query = dict(urllib.parse.parse_qsl(parsed_auth.query))

    # Merge new parameters, giving precedence to the new ones
    merged_query = {**auth_query, **query_params}
    encoded_query = urllib.parse.urlencode(merged_query)

    # Reconstruct the full URL
    new_url_parts = parsed_auth._replace(query=encoded_query)
    sso_url = urllib.parse.urlunparse(new_url_parts)

    return sso_url