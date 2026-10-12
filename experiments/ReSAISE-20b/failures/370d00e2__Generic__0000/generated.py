import urllib.parse

# Example set of domains that are allowed for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.myapp.io",
    "localhost:8000",
}

def generate_oauth_token_url(app_base_url: str, token_path: str, session_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g. "https://myapp.com").
    token_path : str
        The relative path to the OAuth callback endpoint (e.g. "/oauth/callback").
    session_state : str
        A cryptographically random string used as the OAuth state parameter.

    Returns
    -------
    str
        The fully-qualified callback URL including the `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in
        :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Normalise the base URL and token path
    parsed_base = urllib.parse.urlparse(app_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {app_base_url!r}")

    # Ensure the token path starts with a slash
    normalized_path = urllib.parse.quote(token_path.lstrip("/"))
    if not token_path.startswith("/"):
        normalized_path = "/" + normalized_path

    # Build the full URL
    url_parts = parsed_base._replace(path=normalized_path)
    base_url_without_query = urllib.parse.urlunparse(url_parts)

    # Append the state query parameter
    query = urllib.parse.urlencode({"state": session_state})
    full_url = f"{base_url_without_query}?{query}"

    # Validate the domain
    parsed_full = urllib.parse.urlparse(full_url)
    if parsed_full.netloc not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Unauthorized callback domain: {parsed_full.netloc!r}")

    return full_url