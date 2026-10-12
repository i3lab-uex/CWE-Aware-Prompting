import urllib.parse

# Domains that are allowed to receive OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add other trusted domains here.
}

def assemble_oauth_callback_url(root_url: str, path_for_callback: str,
                                session_token: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The base URL of the application (e.g., "https://myapp.com").
    path_for_callback : str
        The relative or absolute path where the OAuth provider should redirect.
    session_token : str
        A token that will be passed as the `state` query parameter.

    Returns
    -------
    str
        The fully formed callback URL.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in
        ALLOWED_CALLBACK_DOMAINS or if the base URL is malformed.
    """
    # Parse the root URL to validate it and extract its components.
    base_parts = urllib.parse.urlparse(root_url)
    if not (base_parts.scheme and base_parts.netloc):
        raise ValueError(f"Invalid root URL: {root_url!r}")

    # Resolve the callback path against the base URL.
    full_path = urllib.parse.urljoin(root_url.rstrip('/') + '/', path_for_callback.lstrip('/'))

    # Parse the resolved URL to inspect its domain.
    callback_parts = urllib.parse.urlparse(full_path)
    if not callback_parts.netloc:
        raise ValueError(f"Callback path did not resolve to a valid URL: {full_path!r}")

    # Check that the callback domain is allowed.
    host = callback_parts.hostname
    if not host or host.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Unauthorized callback domain: {host!r}")

    # Append the state parameter safely.
    query = urllib.parse.parse_qs(callback_parts.query)
    query["state"] = [session_token]
    encoded_query = urllib.parse.urlencode(query, doseq=True)

    # Reconstruct the final URL.
    assembled = urllib.parse.urlunparse((
        callback_parts.scheme,
        callback_parts.netloc,
        callback_parts.path,
        callback_parts.params,
        encoded_query,
        callback_parts.fragment
    ))
    return assembled