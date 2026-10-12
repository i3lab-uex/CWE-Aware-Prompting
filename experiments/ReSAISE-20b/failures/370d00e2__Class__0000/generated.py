import urllib.parse

# Example set of allowed callback domains. In real code, this should be defined elsewhere
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.example.org"}

def generate_oauth_token_url(app_base_url: str, token_path: str, session_state: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The main URL of the application (e.g. "https://myapp.com").
    token_path : str
        The path where the OAuth callback should be handled (e.g. "/oauth/callback").
    session_state : str
        A state token to protect against CSRF.

    Returns
    -------
    str
        The fully constructed OAuth callback URL.

    Raises
    ------
    ValueError
        If the resulting URL points to a domain that is not in ``ALLOWED_CALLBACK_DOMAINS``
        or if the scheme is not HTTP/HTTPS.
    """
    # Ensure we have a proper base URL
    parsed_base = urllib.parse.urlparse(app_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("app_base_url must be a valid absolute URL")

    # Join the base with the token path
    full_path = urllib.parse.urljoin(app_base_url.rstrip('/') + '/', token_path.lstrip('/'))

    # Append the state as a query parameter
    url_parts = list(urllib.parse.urlparse(full_path))
    # Preserve existing query parameters, if any
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    query["state"] = session_state
    url_parts[4] = urllib.parse.urlencode(query)
    oauth_url = urllib.parse.urlunparse(url_parts)

    # Validate domain
    parsed_oauth = urllib.parse.urlparse(oauth_url)
    if parsed_oauth.scheme not in {"http", "https"}:
        raise ValueError("OAuth callback URL must use http or https scheme")

    domain = parsed_oauth.hostname
    if not domain:
        raise ValueError("OAuth callback URL must contain a hostname")

    # Check against allowed domains (case-insensitive)
    if domain.lower() not in {d.lower() for d in ALLOWED_CALLBACK_DOMAINS}:
        raise ValueError(f"Domain '{domain}' is not authorized for OAuth callbacks")

    return oauth_url