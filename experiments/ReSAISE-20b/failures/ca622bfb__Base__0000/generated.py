import urllib.parse

# Set of domains that are allowed for OAuth callback URLs.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.example.org"}

def assemble_oauth_callback_url(root_url: str, path_for_callback: str,
                                session_token: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The base URL of the application (e.g. "https://app.example.com").
    path_for_callback : str
        The relative path that will handle the OAuth callback.
    session_token : str
        A token to include as a query parameter for CSRF protection.

    Returns
    -------
    str
        The fully-qualified OAuth callback URL.

    Raises
    ------
    ValueError
        If the resulting URL points to a domain that is not in
        ALLOWED_CALLBACK_DOMAINS.
    """
    # Ensure the root URL has a scheme; if missing, assume https
    parsed_root = urllib.parse.urlparse(root_url)
    if not parsed_root.scheme:
        root_url = f"https://{root_url}"
        parsed_root = urllib.parse.urlparse(root_url)

    # Join the root URL with the callback path
    full_path = urllib.parse.urljoin(root_url, path_for_callback)

    # Add the state parameter
    query = urllib.parse.urlencode({"state": session_token})
    callback_url = f"{full_path}?{query}"

    # Validate the domain of the resulting URL
    callback_netloc = urllib.parse.urlparse(callback_url).netloc.lower()
    # Strip possible port
    domain = callback_netloc.split(":")[0]

    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Unauthorized callback domain: {domain}")

    return callback_url