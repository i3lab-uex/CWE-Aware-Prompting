import urllib.parse

# Whitelist of domains that can be used as return URLs.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add more domains as needed
}

def build_sso_url(sso_path: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL.

    Parameters
    ----------
    sso_path : str
        The base SSO endpoint URL (may already contain query parameters).
    uid : str
        Unique user identifier to be passed to the SSO provider.
    redirect_url : str
        The URL to which the user should be returned after authentication.

    Returns
    -------
    str
        The fully constructed SSO redirect URL.

    Raises
    ------
    ValueError
        If the domain of `redirect_url` is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Parse the redirect URL and ensure it uses an allowed domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_url must be a fully qualified URL")

    # Extract the domain (netloc may include port)
    domain = parsed_redirect.hostname
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not allowed for return URLs")

    # Parse the SSO path
    parsed_sso = urllib.parse.urlparse(sso_path)

    # Merge existing query parameters with the new ones
    sso_query = dict(urllib.parse.parse_qsl(parsed_sso.query, keep_blank_values=True))
    sso_query.update({
        "uid": uid,
        "returnUrl": redirect_url
    })

    # Reconstruct the SSO URL with updated query string
    new_sso = parsed_sso._replace(query=urllib.parse.urlencode(sso_query, doseq=True))
    return urllib.parse.urlunparse(new_sso)