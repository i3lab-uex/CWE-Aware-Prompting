import urllib.parse

# Example allowed domains; replace with actual values in production.
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
        The base URL of the application (e.g., "https://myapp.com").
    token_path : str
        The path that handles OAuth callbacks (e.g., "/oauth/callback").
    session_state : str
        A unique state token used to prevent CSRF.

    Returns
    -------
    str
        The fully-qualified callback URL including the state query parameter.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain not in `ALLOWED_CALLBACK_DOMAINS`
        or if the base URL is malformed.
    """
    # Parse the base URL to validate it and extract components
    parsed_base = urllib.parse.urlparse(app_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {app_base_url!r}")

    # Ensure the domain is allowed
    host = parsed_base.hostname or ""
    if host.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Domain {host!r} is not allowed for OAuth callbacks")

    # Join the base URL with the token path
    joined = urllib.parse.urljoin(app_base_url.rstrip('/') + '/', token_path.lstrip('/'))

    # Append the state parameter
    url_parts = list(urllib.parse.urlparse(joined))
    query = urllib.parse.parse_qs(url_parts[4])
    query["state"] = [session_state]
    url_parts[4] = urllib.parse.urlencode(query, doseq=True)

    return urllib.parse.urlunparse(url_parts)