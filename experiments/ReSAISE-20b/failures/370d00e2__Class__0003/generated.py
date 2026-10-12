import urllib.parse

# Example allowed domains; in real code these would be set elsewhere.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.myapp.org"}


def generate_oauth_token_url(app_base_url: str, token_path: str, session_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g., "https://myapp.com").
    token_path : str
        The path to the OAuth callback endpoint (e.g., "/oauth/callback").
    session_state : str
        A cryptographically random string used as the OAuth state parameter.

    Returns
    -------
    str
        The fully qualified callback URL.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in
        :data:`ALLOWED_CALLBACK_DOMAINS` or if the URL scheme is missing.
    """
    # Ensure we have a proper base URL
    parsed_base = urllib.parse.urlparse(app_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("app_base_url must be a fully qualified URL")

    # Join base and path safely
    callback_path = urllib.parse.urljoin(parsed_base.path + "/", token_path.lstrip("/"))
    # Build query string
    query = urllib.parse.urlencode({"state": session_state})
    # Construct the full URL
    callback_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            callback_path,
            "",  # params
            query,
            "",  # fragment
        )
    )

    # Validate domain against allowed list (CWE-610 mitigation)
    parsed_callback = urllib.parse.urlparse(callback_url)
    domain = parsed_callback.hostname
    if not domain or domain.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Unauthorized callback domain: {domain}")

    return callback_url