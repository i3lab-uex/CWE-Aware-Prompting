import urllib.parse

# Set of domains that are allowed to receive OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    "localhost",  # for local development
}

def generate_oauth_token_url(app_base_url: str, token_path: str, session_state: str) -> str:
    """
    Construct a full OAuth callback URL and validate its domain.

    Parameters
    ----------
    app_base_url : str
        Base URL of the application (e.g., "https://myapp.com").
    token_path : str
        Path segment that triggers the OAuth callback (e.g., "/oauth/callback").
    session_state : str
        State parameter used to protect against CSRF attacks.

    Returns
    -------
    str
        Fully-qualified OAuth callback URL.

    Raises
    ------
    ValueError
        If the constructed URL is malformed or its domain is not in
        :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Ensure the base URL has a scheme; default to https if missing
    parsed_base = urllib.parse.urlparse(app_base_url)
    if not parsed_base.scheme:
        app_base_url = f"https://{app_base_url}"
        parsed_base = urllib.parse.urlparse(app_base_url)

    # Join the base URL with the token path
    callback_path = urllib.parse.urljoin(parsed_base.path, token_path)

    # Build the query string with state
    query = urllib.parse.urlencode({"state": session_state})

    # Assemble the final URL
    callback_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        callback_path,
        "",  # params
        query,
        ""   # fragment
    ))

    # Validate domain
    callback_netloc = urllib.parse.urlparse(callback_url).netloc
    host = callback_netloc.split(":")[0]  # strip port if present

    if host not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Unauthorized callback domain: '{host}'. "
            f"Allowed domains are: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
        )

    return callback_url