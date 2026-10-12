import urllib.parse

# Whitelist of domains that are allowed as redirect targets.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    "trusted-site.net"
}

def create_sso_url(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Construct a secure SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        The base SSO endpoint URL.
    uid : str
        Unique user identifier to be passed to the identity provider.
    redirect_url : str
        The URL to which the user should be returned after authentication.

    Returns
    -------
    str
        The full SSO redirect URL ready to be sent to the user.

    Raises
    ------
    ValueError
        If `redirect_url` does not belong to an allowed domain.
    """
    # Parse the redirect URL and validate its domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_url must be an absolute URL")

    # Normalize domain: strip port and lower case
    domain = parsed_redirect.hostname.lower() if parsed_redirect.hostname else ""
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"redirect_url domain '{domain}' is not allowed")

    # Build query parameters for the SSO endpoint
    params = {
        "uid": uid,
        # The redirect URL must be percent‑encoded
        "redirect_uri": urllib.parse.quote_plus(redirect_url)
    }
    query_string = urllib.parse.urlencode(params)

    # Ensure auth_endpoint does not already contain a query string
    parsed_auth = urllib.parse.urlparse(auth_endpoint)
    if parsed_auth.query:
        raise ValueError("auth_endpoint must not contain query parameters")

    # Assemble the final URL
    sso_url = urllib.parse.urlunparse((
        parsed_auth.scheme,
        parsed_auth.netloc,
        parsed_auth.path,
        "",  # params
        query_string,  # query
        ""   # fragment
    ))
    return sso_url