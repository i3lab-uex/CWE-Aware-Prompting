import urllib.parse

# Example list of allowed callback domains; replace with your actual whitelist.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    "localhost",  # for local development
}

def generate_oauth_callback_link(app_base_url: str,
                                 callback_endpoint: str,
                                 verification_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g. "https://myapp.com").
    callback_endpoint : str
        The path where the OAuth provider should redirect to (e.g. "/auth/callback").
    verification_state : str
        A unique state string to protect against CSRF attacks.

    Returns
    -------
    str
        The fully-qualified callback URL with the state query parameter appended.

    Raises
    ------
    ValueError
        If the domain of the resulting URL is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Ensure the base URL ends with a slash so that urljoin behaves predictably.
    base = app_base_url.rstrip('/') + '/'
    # Resolve the full path (handles leading/trailing slashes in callback_endpoint).
    resolved_path = urllib.parse.urljoin(base, callback_endpoint.lstrip('/'))

    # Append the state parameter. We use urlencode to ensure proper escaping.
    query = urllib.parse.urlencode({"state": verification_state})
    callback_url = f"{resolved_path}?{query}"

    # Parse the URL to extract the hostname for domain validation.
    parsed = urllib.parse.urlparse(callback_url)
    host = parsed.hostname
    if not host:
        raise ValueError("Resulting callback URL does not contain a hostname.")

    # Verify that the host is in the allowed list (case-insensitive).
    if host.lower() not in {d.lower() for d in ALLOWED_CALLBACK_DOMAINS}:
        raise ValueError(f"Disallowed callback domain: {host}")

    return callback_url