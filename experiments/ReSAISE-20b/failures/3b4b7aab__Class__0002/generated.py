import urllib.parse

# Example set of allowed callback domains. In real code this should be configured securely.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.myapp.org"}

def construct_oauth_callback_uri(root_url: str, callback_uri: str, session_state: str) -> str:
    """
    Construct a fully qualified OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The application's base URL, e.g. "https://myapp.example.com".
    callback_uri : str
        The path for the OAuth callback endpoint, e.g. "/oauth/callback".
    session_state : str
        A unique value to include as the `state` query parameter.

    Returns
    -------
    str
        The full callback URL including the `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    if not root_url or not callback_uri:
        raise ValueError("Both `root_url` and `callback_uri` must be provided")

    # Build the base URL by joining root_url with callback_uri.
    # urljoin handles leading/trailing slashes correctly.
    base_callback = urllib.parse.urljoin(root_url.rstrip('/') + '/', callback_uri.lstrip('/'))

    # Parse the resulting URL to inspect its components.
    parsed = urllib.parse.urlparse(base_callback)

    # Ensure the scheme is present and secure (https preferred).
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Verify the host/domain is allowed.
    domain = parsed.hostname
    if not domain or domain.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not allowed for OAuth callbacks")

    # Append the state query parameter safely.
    query_params = urllib.parse.parse_qs(parsed.query)
    # `parse_qs` returns lists; we want a single value.
    query_params["state"] = [session_state]
    # Build the new query string.
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the full URL with the new query.
    final_url = urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))

    return final_url