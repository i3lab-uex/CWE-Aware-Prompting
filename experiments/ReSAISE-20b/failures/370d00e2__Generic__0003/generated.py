import urllib.parse

# Domains allowed to be used as OAuth callback endpoints.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "myapp.example.org",
    # Add any other approved domains here.
}


def generate_oauth_token_url(app_base_url: str, token_path: str, session_state: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g., "https://myapp.example.org").
    token_path : str
        The relative path that will handle the OAuth callback
        (e.g., "/auth/callback").
    session_state : str
        A random string used to verify the OAuth transaction.

    Returns
    -------
    str
        The fully-qualified callback URL including the state query parameter.

    Raises
    ------
    ValueError
        If the resolved callback URL resolves to a domain that is not in
        ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Parse the base URL to isolate its components
    parsed_base = urllib.parse.urlparse(app_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {app_base_url!r}")

    # Ensure the domain is allowed
    host = parsed_base.hostname.lower()
    if host not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Domain '{host}' is not allowed for OAuth callbacks")

    # Join the path safely
    callback_path = urllib.parse.urljoin(parsed_base.path or "/", token_path.lstrip("/"))

    # Build query parameters, ensuring the state is safely encoded
    query = urllib.parse.urlencode({"state": session_state})

    # Reconstruct the full URL
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

    return callback_url