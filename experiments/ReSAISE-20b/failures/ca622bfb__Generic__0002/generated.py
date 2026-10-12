import urllib.parse

# Example set of allowed callback domains; replace with real values.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.myapp.org",
}

def assemble_oauth_callback_url(root_url: str, path_for_callback: str, session_token: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The base URL of the application (e.g. "https://myapp.com").
    path_for_callback : str
        The relative path to the callback endpoint (e.g. "/oauth/callback").
    session_token : str
        A unique token to be sent as the ``state`` query parameter.

    Returns
    -------
    str
        The fully qualified callback URL, including the ``state`` parameter.

    Raises
    ------
    ValueError
        If the resulting URL has an unsupported scheme or its domain is not in
        :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Ensure root_url has a scheme; otherwise, prepend https.
    parsed_root = urllib.parse.urlparse(root_url)
    if not parsed_root.scheme:
        root_url = f"https://{root_url}"
        parsed_root = urllib.parse.urlparse(root_url)

    # Build the full path
    callback_path = urllib.parse.urljoin(parsed_root.path + "/", path_for_callback.lstrip("/"))

    # Construct the full URL
    url_parts = list(parsed_root)
    url_parts[2] = callback_path  # path
    query_dict = {"state": session_token}
    url_parts[4] = urllib.parse.urlencode(query_dict)  # query
    full_url = urllib.parse.urlunparse(url_parts)

    # Validate the domain
    parsed_full = urllib.parse.urlparse(full_url)
    if parsed_full.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed_full.scheme}")

    # Extract hostname (without port)
    hostname = parsed_full.hostname
    if not hostname or hostname.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Callback domain '{hostname}' is not authorized")

    return full_url