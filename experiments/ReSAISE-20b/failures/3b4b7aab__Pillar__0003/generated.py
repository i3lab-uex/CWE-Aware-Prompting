import urllib.parse

# Domains that are allowed to be used as OAuth callback endpoints.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    "oauth.myapp.net",
}

def construct_oauth_callback_uri(root_url: str, callback_uri: str, session_state: str) -> str:
    """
    Construct a fully-qualified OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The base URL of the application (e.g. "https://myapp.com").
    callback_uri : str
        The path or full URL for the OAuth callback endpoint.
        If it is a relative path (e.g. "/auth/callback"), it will be joined
        with `root_url`. If it is an absolute URL, it will be used as-is.
    session_state : str
        A unique string that should be passed back to the OAuth provider
        for CSRF protection.

    Returns
    -------
    str
        The fully-qualified callback URL with a ``state`` query parameter.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Resolve the callback URL relative to the root if it is not absolute.
    parsed_callback = urllib.parse.urlparse(callback_uri)
    if not parsed_callback.scheme:
        # Treat callback_uri as a relative path.
        full_url = urllib.parse.urljoin(root_url, callback_uri)
    else:
        # Use the provided absolute URL.
        full_url = callback_uri

    # Append or update the state query parameter.
    parsed_full = urllib.parse.urlparse(full_url)
    query_params = dict(urllib.parse.parse_qsl(parsed_full.query))
    query_params["state"] = session_state
    new_query = urllib.parse.urlencode(query_params)

    # Rebuild the URL with the updated query string.
    safe_url = urllib.parse.urlunparse(
        (
            parsed_full.scheme,
            parsed_full.netloc,
            parsed_full.path,
            parsed_full.params,
            new_query,
            parsed_full.fragment,
        )
    )

    # Verify the domain is allowed.
    domain = urllib.parse.urlparse(safe_url).netloc.lower()
    # Strip port if present.
    domain = domain.split(":")[0]
    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Callback URL domain '{domain}' is not allowed")

    return safe_url