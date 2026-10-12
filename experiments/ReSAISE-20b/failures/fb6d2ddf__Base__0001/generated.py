import urllib.parse

# Whitelisted domains that may be used as the redirect target after SSO.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "myapp.example.org",
    "trusted-site.net",
}

def create_sso_url(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        Base URL of the SSO provider.
    uid : str
        User identifier to be sent as part of the query string.
    redirect_url : str
        The URL where the user should be sent after authentication.

    Returns
    -------
    str
        A fully‑qualified URL that can be used to redirect the user.

    Raises
    ------
    ValueError
        If ``redirect_url`` points to a domain that is not in
        :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the supplied redirect URL to extract its domain.
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_url must be a valid absolute URL")

    # Normalize the domain (remove leading www. if present).
    host = parsed_redirect.netloc.lower()
    if host.startswith("www."):
        host = host[4:]

    # Verify the domain is in the whitelist.
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Domain '{host}' is not allowed for redirect")

    # Construct the query parameters.
    params = {
        "uid": uid,
        "returnUrl": redirect_url,  # keep the original URL; will be encoded below
    }
    query = urllib.parse.urlencode(params, safe=":/?#[]@!$&'()*+,;=%")

    # Build the final SSO URL.
    sso_url = urllib.parse.urljoin(auth_endpoint, "?") + query
    return sso_url