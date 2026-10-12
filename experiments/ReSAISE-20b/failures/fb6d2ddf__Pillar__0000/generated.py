import urllib.parse

# Example whitelist of domains allowed for the return URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "myapp.org",
    "trusted.example.net"
}

def create_sso_url(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Build an SSO redirect URL that points the user to an external identity provider.
    
    Parameters
    ----------
    auth_endpoint : str
        Base URL of the SSO provider (e.g. "https://sso.example.com/auth").
    uid : str
        Unique user identifier to be sent to the provider.
    redirect_url : str
        Destination URL that the provider should redirect back to after authentication.
    
    Returns
    -------
    str
        A fully-formed URL that the user can be redirected to.
    
    Raises
    ------
    ValueError
        If ``redirect_url`` is not an absolute URL or its domain is not in
        :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate that the redirect URL is absolute
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_url must be an absolute URL with scheme and host")

    # Strip port for domain comparison
    host = parsed_redirect.hostname or ""
    if host.lower() not in (d.lower() for d in ALLOWED_RETURN_DOMAINS):
        raise ValueError(f"Redirect domain '{host}' is not in the allowed list")

    # Build query parameters
    params = {
        "uid": uid,
        "redirect_url": redirect_url
    }
    query_string = urllib.parse.urlencode(params, safe=":/?#[]@!$&'()*+,;=")

    # Combine the SSO endpoint with query parameters
    parsed_auth = urllib.parse.urlparse(auth_endpoint)
    # Preserve existing query parameters on the auth endpoint
    if parsed_auth.query:
        full_query = f"{parsed_auth.query}&{query_string}"
    else:
        full_query = query_string

    sso_url = urllib.parse.urlunparse((
        parsed_auth.scheme,
        parsed_auth.netloc,
        parsed_auth.path,
        parsed_auth.params,
        full_query,
        parsed_auth.fragment
    ))

    return sso_url