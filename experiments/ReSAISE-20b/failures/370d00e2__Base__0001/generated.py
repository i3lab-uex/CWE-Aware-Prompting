import urllib.parse

# Example set of allowed callback domains.
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
        Base URL of the application (e.g., "https://myapp.com").
    token_path : str
        Path for the OAuth callback (e.g., "/oauth/callback").
    session_state : str
        State value to include as a query parameter for CSRF protection.

    Returns
    -------
    str
        Full OAuth callback URL with the state parameter appended.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain not in `ALLOWED_CALLBACK_DOMAINS`.
    """
    # Ensure base URL has a scheme
    if not urllib.parse.urlparse(app_base_url).scheme:
        raise ValueError("app_base_url must include a scheme (http:// or https://)")

    # Join base and path safely
    callback_url = urllib.parse.urljoin(app_base_url.rstrip('/') + '/', token_path.lstrip('/'))

    # Parse the URL to inspect its components
    parsed = urllib.parse.urlparse(callback_url)

    # Validate domain against the allowed list (case‑insensitive)
    netloc = parsed.netloc.split(':')[0]  # strip port if present
    if not netloc.lower() in {d.lower() for d in ALLOWED_CALLBACK_DOMAINS}:
        raise ValueError(f"Unauthorized callback domain: {netloc}")

    # Append the state query parameter
    query_params = urllib.parse.parse_qs(parsed.query)
    query_params['state'] = [session_state]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the full URL
    final_url = urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))

    return final_url