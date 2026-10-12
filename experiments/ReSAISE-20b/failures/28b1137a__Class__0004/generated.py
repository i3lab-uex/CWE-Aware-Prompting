import urllib.parse

# Whitelist of domains allowed for the redirect URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    # Add more domains as required
}

def build_sso_url(sso_path: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL that includes the user ID and a safe return URL.

    Parameters
    ----------
    sso_path : str
        The base SSO endpoint (may already contain a query string).
    uid : str
        Unique identifier of the user.
    redirect_url : str
        Destination URL to return after SSO completion.

    Returns
    -------
    str
        Fully-qualified redirect URL that can be sent to the client.

    Raises
    ------
    ValueError
        If the redirect URL's domain is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Validate the redirect URL's domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_url must be an absolute URL")

    # Extract the hostname (strip port if present)
    host = parsed_redirect.hostname.lower()
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Domain '{host}' is not allowed for redirect URLs")

    # Parse the SSO endpoint to manipulate its query string safely
    parsed_sso = urllib.parse.urlparse(sso_path)
    sso_query = dict(urllib.parse.parse_qsl(parsed_sso.query, keep_blank_values=True))

    # Add/override required parameters
    sso_query.update({
        "uid": uid,
        "redirect_url": redirect_url,  # will be URL‑encoded by urlencode
    })

    # Reconstruct the full SSO URL
    new_query = urllib.parse.urlencode(sso_query, doseq=True)
    sso_url_parts = (
        parsed_sso.scheme,
        parsed_sso.netloc,
        parsed_sso.path,
        parsed_sso.params,
        new_query,
        parsed_sso.fragment,
    )
    return urllib.parse.urlunparse(sso_url_parts)