import urllib.parse

# Example set of allowed callback domains.  In a real application this should be
# defined in configuration and kept up to date.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.myapp.io"}

def generate_oauth_token_url(app_base_url: str, token_path: str,
                             session_state: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        Base URL of the application, e.g. "https://myapp.com".
    token_path : str
        Path that will handle the OAuth callback, e.g. "/oauth/callback".
    session_state : str
        State token used to prevent CSRF attacks.

    Returns
    -------
    str
        The fully qualified callback URL including the state query parameter.

    Raises
    ------
    ValueError
        If the resulting URL does not belong to an allowed domain.
    """
    # Normalise base URL: ensure it has a scheme and no trailing slash
    parsed_base = urllib.parse.urlparse(app_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {app_base_url}")

    # Build the path, stripping any leading/trailing slashes to avoid double
    # separators and then re-adding a single slash.
    base_netloc = parsed_base.netloc
    if base_netloc not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Domain '{base_netloc}' is not allowed for callbacks")

    # Join the base path with the token path
    joined_path = urllib.parse.urljoin(parsed_base.path + '/', token_path.lstrip('/'))

    # Merge any existing query parameters with the state parameter
    base_query = urllib.parse.parse_qs(parsed_base.query)
    # parse_qs returns values as lists; we want simple strings for existing keys
    merged_query = {k: v[0] if isinstance(v, list) else v for k, v in base_query.items()}
    merged_query['state'] = session_state

    # Reconstruct the full URL
    new_url_parts = (
        parsed_base.scheme,
        base_netloc,
        joined_path,
        '',  # params
        urllib.parse.urlencode(merged_query, doseq=True),
        ''   # fragment
    )
    full_url = urllib.parse.urlunparse(new_url_parts)
    return full_url

# Example usage (remove or comment out in production code):
if __name__ == "__main__":
    url = generate_oauth_token_url(
        app_base_url="https://example.com",
        token_path="/oauth/callback",
        session_state="abc123"
    )
    print(url)  # https://example.com/oauth/callback?state=abc123