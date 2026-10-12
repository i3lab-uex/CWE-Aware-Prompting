import urllib.parse

# Example list of domains that are allowed to receive OAuth callbacks.
# In a real application this should be configured via environment variables
# or a secure configuration service and not hard‑coded.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "api.example.com",
}

def construct_oauth_callback_uri(root_url: str, callback_uri: str,
                                 session_state: str) -> str:
    """
    Build a fully qualified OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The base URL of the application (e.g. "https://app.example.com").
    callback_uri : str
        The path where the OAuth provider should redirect to (e.g. "/oauth/callback").
    session_state : str
        A unique string that should be returned by the OAuth provider to
        validate the request.

    Returns
    -------
    str
        The complete callback URL with a `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # 1. Resolve the callback URL against the root URL.
    # ``urljoin`` handles missing slashes and relative paths correctly.
    full_url = urllib.parse.urljoin(root_url.rstrip('/') + '/', callback_uri.lstrip('/'))

    # 2. Append the `state` query parameter.
    parsed = urllib.parse.urlparse(full_url)
    # Preserve existing query parameters if any.
    query_params = dict(urllib.parse.parse_qsl(parsed.query, keep_blank_values=True))
    query_params['state'] = session_state
    new_query = urllib.parse.urlencode(query_params)

    # Reconstruct the URL with the updated query string.
    final_url = urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))

    # 3. Validate that the domain is allowed.
    domain = parsed.netloc.split(':')[0].lower()  # strip port if present
    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Disallowed callback domain: {domain}")

    return final_url