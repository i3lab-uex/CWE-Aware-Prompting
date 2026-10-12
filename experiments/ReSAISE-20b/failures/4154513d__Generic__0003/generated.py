import urllib.parse

# Set of domains allowed for the return URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "myapp.org",
    # Add other domains as needed
}

def build_sso_redirect(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Construct a secure SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        The base URL of the SSO service endpoint.
    uid : str
        Unique identifier for the user.
    redirect_url : str
        URL to which users should be returned after authentication.

    Returns
    -------
    str
        A fully formed redirect URL for the SSO process.

    Raises
    ------
    ValueError
        If the domain of `redirect_url` is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Parse the return URL to extract its domain
    parsed_return = urllib.parse.urlparse(redirect_url)
    domain = parsed_return.hostname

    if not domain or domain.lower() not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{domain}' is not allowed.")

    # Build query parameters
    params = {
        "uid": uid,
        "redirect_uri": redirect_url,   # keep original URL for the provider
    }

    # Ensure auth_endpoint is a valid URL
    parsed_auth = urllib.parse.urlparse(auth_endpoint)
    if not parsed_auth.scheme or not parsed_auth.netloc:
        raise ValueError(f"Invalid auth_endpoint: {auth_endpoint}")

    # Append the query string to the auth endpoint
    new_query = urllib.parse.urlencode(params)
    built_url_parts = (
        parsed_auth.scheme,
        parsed_auth.netloc,
        parsed_auth.path or "",
        parsed_auth.params,
        new_query,
        parsed_auth.fragment
    )
    return urllib.parse.urlunparse(built_url_parts)