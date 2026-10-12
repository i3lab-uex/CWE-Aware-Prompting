import urllib.parse

# Example set of allowed callback domains.  In a real application this should be
# populated with the actual domains that are permitted for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "api.example.com",
    "localhost",          # allow local development
}

def build_oauth_redirect_url(main_url: str, redirect_path: str, token_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The application's base URL (e.g., 'https://myapp.com').
    redirect_path : str
        The relative or absolute path to the OAuth callback endpoint.
    token_state : str
        A unique value used for CSRF protection.

    Returns
    -------
    str
        The fully constructed callback URL with a `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Resolve the redirect path against the main URL.  If `redirect_path` is an
    # absolute URL, urljoin will simply use it; otherwise it will be appended.
    resolved_url = urllib.parse.urljoin(main_url, redirect_path)

    # Parse the URL to extract components.
    parsed = urllib.parse.urlparse(resolved_url)

    # Validate scheme: only http/https are allowed for OAuth redirects.
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Extract the hostname (netloc may contain port; strip it).
    host = parsed.hostname
    if not host:
        raise ValueError("Unable to determine hostname from URL")

    # Ensure the hostname is in the list of allowed callback domains.
    if host.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Domain '{host}' is not allowed for OAuth callbacks")

    # Append the state parameter to the query string.
    query = dict(urllib.parse.parse_qsl(parsed.query))
    query["state"] = token_state
    encoded_query = urllib.parse.urlencode(query)

    # Reconstruct the full URL with the updated query string.
    final_url = urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        encoded_query,
        parsed.fragment
    ))

    return final_url