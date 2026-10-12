import urllib.parse

# Allowed domains for OAuth callback URLs.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.example.org"}

def create_oauth_callback_url(base_url: str, callback_path: str, state: str) -> str:
    """
    Build a fully-qualified OAuth callback URL from the base application URL,
    a relative callback path, and a state parameter.

    Parameters
    ----------
    base_url : str
        The base URL of the application (must include scheme, e.g. "https://app.example.com").
    callback_path : str
        The relative path to the OAuth callback endpoint (e.g. "/auth/callback").
    state : str
        A unique opaque string used to maintain state between request and callback.

    Returns
    -------
    str
        The complete OAuth callback URL with the state query parameter appended.

    Raises
    ------
    ValueError
        If the resulting callback URL resolves to a domain that is not in
        ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Ensure the callback path is a proper relative URL
    if not callback_path.startswith("/"):
        raise ValueError("callback_path must start with '/'")

    # Join base URL and callback path safely
    full_url = urllib.parse.urljoin(base_url, callback_path)

    # Append the state parameter
    parsed = urllib.parse.urlparse(full_url)
    query_params = dict(urllib.parse.parse_qsl(parsed.query))
    query_params["state"] = state
    new_query = urllib.parse.urlencode(query_params)

    # Reconstruct the URL with the updated query string
    final_url = urllib.parse.urlunparse(
        parsed._replace(query=new_query)
    )

    # Validate the domain against the allowed set
    hostname = urllib.parse.urlparse(final_url).hostname
    if not hostname or hostname.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Disallowed callback domain: {hostname}")

    return final_url