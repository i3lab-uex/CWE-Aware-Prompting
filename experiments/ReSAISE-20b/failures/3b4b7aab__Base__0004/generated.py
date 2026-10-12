import urllib.parse

# Domains that are considered safe for OAuth callback URLs.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    "subdomain.safe-domain.net",
}


def construct_oauth_callback_uri(root_url: str, callback_uri: str, session_state: str) -> str:
    """
    Construct a fully‑qualified OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The application's base URL (e.g. "https://myapp.com").
    callback_uri : str
        The relative path for the OAuth callback (e.g. "/auth/callback").
    session_state : str
        A unique value used to verify the integrity of the OAuth flow.

    Returns
    -------
    str
        The complete callback URL, e.g.
        "https://myapp.com/auth/callback?state=abc123".

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in
        ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # 1. Ensure callback_uri is a relative path (no scheme or netloc)
    parsed_cb = urllib.parse.urlparse(callback_uri)
    if parsed_cb.scheme or parsed_cb.netloc:
        raise ValueError("callback_uri must be a relative path")

    # 2. Combine root_url with callback_uri safely
    full_path = urllib.parse.urljoin(root_url.rstrip("/") + "/", parsed_cb.path.lstrip("/"))

    # 3. Append the state parameter
    query = urllib.parse.urlencode({"state": session_state})
    callback_url = f"{full_path}?{query}"

    # 4. Validate the domain
    parsed_url = urllib.parse.urlparse(callback_url)
    host = parsed_url.hostname or ""
    if host not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Domain '{host}' is not allowed for OAuth callbacks")

    return callback_url