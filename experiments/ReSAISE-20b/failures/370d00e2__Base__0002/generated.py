import urllib.parse

# Set of domains that are allowed to receive OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.example.org"}

def generate_oauth_token_url(app_base_url: str, token_path: str, session_state: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The main URL of the application (e.g., "https://myapp.com").
    token_path : str
        The path that handles the OAuth callback (e.g., "/oauth/callback").
    session_state : str
        A state token used to protect against CSRF attacks.

    Returns
    -------
    str
        The fully qualified callback URL with the state query parameter appended.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain not in ALLOWED_CALLBACK_DOMAINS.
    """
    # Normalise the base URL and token path
    base = app_base_url.rstrip("/") + "/"
    # Ensure the token_path is relative (no leading scheme or netloc)
    parsed_token = urllib.parse.urlparse(token_path)
    if parsed_token.scheme or parsed_token.netloc:
        # token_path should not be an absolute URL
        raise ValueError("token_path must be a relative path, not a full URL")
    # Join base and token_path
    callback_url = urllib.parse.urljoin(base, parsed_token.path.lstrip("/"))

    # Append the state parameter
    query = urllib.parse.urlencode({"state": session_state})
    callback_url_with_query = (
        urllib.parse.urldefrag(callback_url)[0]  # remove any fragment
    ) + "?" + query

    # Validate the domain
    parsed = urllib.parse.urlparse(callback_url_with_query)
    if parsed.netloc.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Callback domain '{parsed.netloc}' is not allowed")

    return callback_url_with_query