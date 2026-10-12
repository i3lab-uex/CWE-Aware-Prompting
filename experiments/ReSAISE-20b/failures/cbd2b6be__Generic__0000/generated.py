import urllib.parse

# Domains that are permitted to receive OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    "localhost",
}

def build_oauth_redirect_url(main_url: str, redirect_path: str, token_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g. "https://app.example.com").
    redirect_path : str
        The path component for the OAuth callback (e.g. "/auth/callback").
    token_state : str
        A unique value to protect against CSRF attacks.

    Returns
    -------
    str
        The fully formed callback URL with the state parameter appended.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Join the base URL with the callback path
    full_url = urllib.parse.urljoin(main_url.rstrip('/') + '/', redirect_path.lstrip('/'))

    # Parse the URL to manipulate query parameters safely
    parsed = urllib.parse.urlparse(full_url)

    # Extract existing query params and add the state
    query_params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    # parse_qs returns lists for each key; flatten to single values for urlencode
    flat_query = {k: v[0] if isinstance(v, list) else v for k, v in query_params.items()}
    flat_query["state"] = token_state

    # Reconstruct the URL with updated query string
    new_query = urllib.parse.urlencode(flat_query)
    secured_url = parsed._replace(query=new_query).geturl()

    # Validate domain against allowed list
    hostname = urllib.parse.urlparse(secured_url).hostname or ""
    if hostname.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Disallowed callback domain: {hostname}")

    return secured_url