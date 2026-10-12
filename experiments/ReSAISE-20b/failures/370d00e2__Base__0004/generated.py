import urllib.parse

# Domains that are allowed to receive OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
}

def generate_oauth_token_url(app_base_url: str, token_path: str, session_state: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g., "https://app.example.com").
    token_path : str
        The path that will handle the OAuth callback (e.g., "/auth/callback").
    session_state : str
        A state string to embed in the query parameters for CSRF protection.

    Returns
    -------
    str
        A fully formed, validated callback URL.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to an allowed domain.
    """
    # Normalise base URL (ensure scheme present)
    parsed_base = urllib.parse.urlparse(app_base_url.rstrip("/"))
    if not parsed_base.scheme:
        raise ValueError(f"Base URL must include a scheme: {app_base_url}")

    # Construct the callback path
    normalized_path = urllib.parse.urljoin(parsed_base.path + "/", token_path.lstrip("/"))

    # Build query string with state
    query = urllib.parse.urlencode({"state": session_state})

    # Assemble the full URL
    callback_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        normalized_path,
        "",  # params
        query,
        ""   # fragment
    ))

    # Validate domain against allowed list
    if parsed_base.netloc.split(":")[0] not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Unauthorized callback domain: {parsed_base.netloc}")

    return callback_url