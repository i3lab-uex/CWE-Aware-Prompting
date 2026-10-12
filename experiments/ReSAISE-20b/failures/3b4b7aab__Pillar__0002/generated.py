import urllib.parse

# Example set of allowed domains for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    "localhost",  # For local testing
}

def construct_oauth_callback_uri(root_url: str, callback_uri: str, session_state: str) -> str:
    """
    Construct a fully qualified OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The base URL of the application (e.g., "https://myapp.com").
    callback_uri : str
        The relative path for the OAuth callback endpoint (e.g., "/auth/callback").
    session_state : str
        A unique value that should be returned by the OAuth provider to
        prevent CSRF attacks.

    Returns
    -------
    str
        A complete URL containing the base, callback path and a `state`
        query parameter.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Resolve the full callback URL
    full_url = urllib.parse.urljoin(root_url, callback_uri)

    # Parse the URL to extract components
    parsed = urllib.parse.urlparse(full_url)

    # Validate domain against allowed list (case-insensitive)
    host = parsed.hostname
    if not host or host.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Callback domain '{host}' is not allowed")

    # Append the state query parameter safely
    query = dict(urllib.parse.parse_qsl(parsed.query))
    query["state"] = session_state
    new_query = urllib.parse.urlencode(query)

    # Rebuild the URL with updated query string
    safe_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment,
        )
    )

    return safe_url