import urllib.parse

# Domains that are considered safe for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    "localhost",      # for local development
}

def build_oauth_redirect_url(main_url: str, redirect_path: str, token_state: str) -> str:
    """
    Construct a fully qualified OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The application's base URL (e.g., "https://app.example.com").
    redirect_path : str
        The path to the callback endpoint (e.g., "/oauth/callback").
    token_state : str
        A unique value to prevent CSRF attacks.

    Returns
    -------
    str
        The complete OAuth callback URL with the state query parameter appended.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in ALLOWED_CALLBACK_DOMAINS.
    """
    # Normalize and combine the base URL with the callback path
    full_url = urllib.parse.urljoin(main_url.rstrip('/') + '/', redirect_path.lstrip('/'))

    # Parse the resulting URL to inspect its components
    parsed = urllib.parse.urlparse(full_url)

    # Extract the hostname (domain) for validation
    domain = parsed.hostname
    if not domain or domain.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Disallowed callback domain: {domain}")

    # Build the query string with the state parameter
    query_params = urllib.parse.parse_qs(parsed.query)
    # Ensure we don't override an existing state parameter
    if "state" in query_params:
        raise ValueError("Callback URL already contains a state parameter.")
    query_params["state"] = [token_state]

    # Reconstruct the URL with the new query string
    new_query = urllib.parse.urlencode(query_params, doseq=True)
    safe_url = parsed._replace(query=new_query).geturl()

    return safe_url