import urllib.parse

# Domains allowed for OAuth callback URLs. Adjust as necessary.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.example.org"}

def assemble_oauth_callback_url(root_url: str, path_for_callback: str, session_token: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The base URL of the application (e.g., "https://app.example.com").
    path_for_callback : str
        The relative path that will handle the OAuth callback (e.g., "/auth/callback").
    session_token : str
        A cryptographically random string used as the OAuth state parameter.

    Returns
    -------
    str
        The fully qualified callback URL, e.g.:
            "https://app.example.com/auth/callback?state=abc123"

    Raises
    ------
    ValueError
        If the resulting domain is not in ALLOWED_CALLBACK_DOMAINS.
    """
    if not all(isinstance(arg, str) for arg in (root_url, path_for_callback, session_token)):
        raise TypeError("All arguments must be strings")

    # Resolve the full callback URL (handles missing slashes gracefully)
    base = urllib.parse.urlparse(root_url)
    if not base.scheme or not base.netloc:
        raise ValueError("root_url must be a valid absolute URL")

    # Construct the path
    callback_path = urllib.parse.urljoin(base.path + "/", path_for_callback.lstrip("/"))

    # Build query parameters
    query = urllib.parse.urlencode({"state": session_token})

    # Assemble the final URL
    callback_url = urllib.parse.urlunparse((
        base.scheme,
        base.netloc,
        callback_path,
        "",      # params
        query,   # query
        ""       # fragment
    ))

    # Validate the domain against allowed domains
    if base.netloc.split(":")[0] not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Domain '{base.netloc}' is not authorized for OAuth callbacks")

    return callback_url