import urllib.parse

# Domains allowed for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add other trusted domains here
}

def generate_oauth_token_url(app_base_url: str, token_path: str, session_state: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g., "https://app.example.com").
    token_path : str
        Path to the OAuth callback endpoint (e.g., "/auth/callback").
    session_state : str
        State parameter to protect against CSRF attacks.

    Returns
    -------
    str
        The fully-qualified callback URL.

    Raises
    ------
    ValueError
        If the resulting domain is not in ALLOWED_CALLBACK_DOMAINS.
    """
    if not app_base_url or not token_path or not session_state:
        raise ValueError("All arguments must be non-empty strings")

    # Ensure token_path is a relative path
    if not token_path.startswith("/"):
        token_path = "/" + token_path

    # Construct the URL
    callback_url = urllib.parse.urljoin(app_base_url, token_path)

    # Append state query parameter safely
    parsed = urllib.parse.urlparse(callback_url)
    query_params = dict(urllib.parse.parse_qsl(parsed.query))
    query_params["state"] = session_state
    new_query = urllib.parse.urlencode(query_params)
    callback_url = parsed._replace(query=new_query).geturl()

    # Verify the domain is allowed
    domain = parsed.netloc.split(":")[0]  # strip port if present
    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not authorized for OAuth callbacks")

    return callback_url