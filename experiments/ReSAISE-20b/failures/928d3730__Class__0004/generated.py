import urllib.parse

# Set of domains that are explicitly allowed for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    "myapp.local",
}

def generate_oauth_url(host_url: str, path_callback: str, session_id: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    host_url : str
        The base URL of the application (e.g., "https://app.example.com").
    path_callback : str
        The endpoint that will handle the OAuth callback.
        Can be an absolute URL or a relative path (e.g., "/auth/callback").
    session_id : str
        A unique identifier that will be sent back as the `state` query parameter.

    Returns
    -------
    str
        The fully assembled callback URL, including the `state` parameter.

    Raises
    ------
    ValueError
        If the resolved callback URL resolves to a domain that is not in
        :data:`ALLOWED_CALLBACK_DOMAINS` and does not match the host's domain.
    """
    # Normalise the host URL so it contains a scheme and netloc
    parsed_host = urllib.parse.urlparse(host_url)
    if not parsed_host.scheme or not parsed_host.netloc:
        raise ValueError(f"Invalid host URL: {host_url!r}")

    # Resolve the callback path against the host URL
    joined = urllib.parse.urljoin(host_url, path_callback)
    parsed_cb = urllib.parse.urlparse(joined)

    # Ensure the callback URL has a scheme and netloc
    if not parsed_cb.scheme or not parsed_cb.netloc:
        raise ValueError(f"Callback path resolved to an invalid URL: {joined!r}")

    # Domain validation
    callback_domain = parsed_cb.hostname.lower() if parsed_cb.hostname else ""
    host_domain = parsed_host.hostname.lower() if parsed_host.hostname else ""

    # Allow callback only if it matches the host domain or is explicitly allowed
    if callback_domain != host_domain and callback_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain {callback_domain!r} is not allowed for OAuth redirects"
        )

    # Build query parameters, preserving any existing ones
    query_params = urllib.parse.parse_qs(parsed_cb.query)
    # Flatten parse_qs output: values are lists, keep first element
    flattened = {k: v[0] for k, v in query_params.items() if v}
    flattened["state"] = session_id

    # Reconstruct the URL with updated query string
    final_parts = (
        parsed_cb.scheme,
        parsed_cb.netloc,
        parsed_cb.path,
        parsed_cb.params,
        urllib.parse.urlencode(flattened, doseq=True),
        parsed_cb.fragment,
    )
    final_url = urllib.parse.urlunparse(final_parts)

    return final_url