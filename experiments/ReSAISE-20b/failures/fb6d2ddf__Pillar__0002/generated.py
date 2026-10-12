import urllib.parse

# Whitelist of allowed domains for the redirect URL.
ALLOWED_RETURN_DOMAINS = {"example.com", "trusted.org"}

def create_sso_url(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        The base SSO endpoint.
    uid : str
        Unique user identifier.
    redirect_url : str
        Destination URL to return after authentication.

    Returns
    -------
    str
        Fully qualified SSO redirect URL with query parameters.

    Raises
    ------
    ValueError
        If the redirect_url domain is not in ALLOWED_RETURN_DOMAINS.
    """
    # Parse the redirect URL to validate its domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_url must be a valid absolute URL")

    # Extract the domain (hostname) and verify against whitelist
    hostname = parsed_redirect.hostname.lower()
    if hostname not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not allowed for redirect URLs")

    # Parse the authentication endpoint and ensure it is absolute
    parsed_auth = urllib.parse.urlparse(auth_endpoint)
    if not parsed_auth.scheme or not parsed_auth.netloc:
        raise ValueError("auth_endpoint must be a valid absolute URL")

    # Build query parameters
    query_params = {
        "uid": uid,
        "redirect_uri": redirect_url,
    }

    # Construct the final URL
    auth_base = urllib.parse.urlunparse(
        (parsed_auth.scheme, parsed_auth.netloc, parsed_auth.path, "", "", "")
    )
    final_url = f"{auth_base}?{urllib.parse.urlencode(query_params)}"
    return final_url