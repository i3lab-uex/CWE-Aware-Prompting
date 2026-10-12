import urllib.parse

# Domains allowed for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "app.example.org",
    "localhost:8000",
}

def generate_oauth_token_url(app_base_url: str, token_path: str, session_state: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The main application URL (e.g. "https://myapp.com").
    token_path : str
        The path where the OAuth callback should be handled (e.g. "/auth/callback").
    session_state : str
        A state token to include in the callback URL for CSRF protection.

    Returns
    -------
    str
        The fully-qualified OAuth callback URL.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Normalize the base URL and path
    parsed_base = urllib.parse.urlparse(app_base_url.rstrip("/"))
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("app_base_url must be a valid URL with scheme and netloc")

    # Construct the callback endpoint
    full_path = urllib.parse.urljoin(parsed_base.path + "/", token_path.lstrip("/"))
    # Build query string with the state parameter
    query = urllib.parse.urlencode({"state": session_state})
    # Assemble the full URL
    callback_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        query,
        ""   # fragment
    ))

    # Validate domain against allowed list
    parsed_callback = urllib.parse.urlparse(callback_url)
    if parsed_callback.netloc not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Unauthorized callback domain: {parsed_callback.netloc}")

    return callback_url