import urllib.parse

# Whitelist of domains that are allowed as return URLs
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "sub.example.com",
    "trusted.org",
}

def build_sso_url(sso_path: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL.

    Parameters
    ----------
    sso_path : str
        Base URL of the SSO endpoint.
    uid : str
        User identifier to be passed as a query parameter.
    redirect_url : str
        URL to which the user will be sent after authentication.

    Returns
    -------
    str
        Full SSO redirect URL with the provided parameters encoded.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect URL to inspect its domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_url must be a full absolute URL")

    # Extract the hostname and compare against allowed domains
    host = parsed_redirect.hostname.lower()
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"redirect_url domain '{host}' is not allowed")

    # Build query parameters
    params = {
        "uid": uid,
        "return_url": redirect_url,
    }
    query_string = urllib.parse.urlencode(params)

    # Construct the final SSO URL
    parsed_sso = urllib.parse.urlparse(sso_path)
    # Preserve existing query params in sso_path, if any
    original_query = parsed_sso.query
    new_query = '&'.join(filter(None, [original_query, query_string]))

    final_url = urllib.parse.urlunparse(
        (
            parsed_sso.scheme,
            parsed_sso.netloc,
            parsed_sso.path,
            parsed_sso.params,
            new_query,
            parsed_sso.fragment,
        )
    )

    return final_url