import urllib.parse

# Domains that are allowed to receive OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "localhost",
    # Add additional trusted domains here.
}

def construct_oauth_callback_uri(root_url: str, callback_uri: str, session_state: str) -> str:
    """
    Construct a fully‑qualified OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The application's base URL (e.g., "https://myapp.com").
    callback_uri : str
        The path to the OAuth callback endpoint (e.g., "/auth/oauth/callback").
    session_state : str
        A unique value used to protect against CSRF attacks.

    Returns
    -------
    str
        The fully qualified callback URL with a `state` query parameter.

    Raises
    ------
    ValueError
        If the domain of the constructed URL is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Resolve the full URL using urllib.parse.urljoin.
    full_url = urllib.parse.urljoin(root_url, callback_uri)

    # Parse the URL components.
    parsed = urllib.parse.urlparse(full_url)

    # Ensure the domain (netloc) is allowed.
    if parsed.netloc not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Callback domain '{parsed.netloc}' is not allowed.")

    # Build the query string, preserving existing parameters if any.
    query_params = urllib.parse.parse_qs(parsed.query)
    # `parse_qs` returns lists for each key; we want a single value.
    query_params = {k: v[0] if isinstance(v, list) else v for k, v in query_params.items()}
    # Add the state parameter.
    query_params["state"] = session_state

    # Reconstruct the URL with the new query string.
    new_query = urllib.parse.urlencode(query_params)
    final_url_parts = parsed._replace(query=new_query)
    return urllib.parse.urlunparse(final_url_parts)