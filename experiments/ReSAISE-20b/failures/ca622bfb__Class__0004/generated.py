import urllib.parse

# Domains that are allowed to receive OAuth callbacks.
# Add any domain you trust here (e.g., 'example.com', 'auth.myapp.com')
ALLOWED_CALLBACK_DOMAINS = {
    # 'example.com',
}

def assemble_oauth_callback_url(root_url: str, path_for_callback: str, session_token: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The base URL of the application (must include scheme, e.g., 'https://myapp.com').
    path_for_callback : str
        The relative or absolute path that will handle the OAuth callback.
    session_token : str
        A cryptographically strong random string used as a state parameter.

    Returns
    -------
    str
        The fully‑qualified callback URL, including the state query parameter.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in ALLOWED_CALLBACK_DOMAINS or if the
        base/root_url is malformed.
    """
    # Validate and parse the root URL
    parsed_root = urllib.parse.urlparse(root_url)
    if not parsed_root.scheme or not parsed_root.netloc:
        raise ValueError(f"Invalid root_url: {root_url!r}")

    # Ensure the callback path is properly joined to the base
    # urllib.parse.urljoin handles relative paths correctly.
    full_path = urllib.parse.urljoin(root_url, path_for_callback)

    # Parse the combined URL to inspect its domain
    parsed_full = urllib.parse.urlparse(full_path)
    if not parsed_full.scheme or not parsed_full.netloc:
        raise ValueError(f"Failed to construct a valid URL from root_url and path: {full_path!r}")

    # Enforce domain whitelist
    if parsed_full.hostname not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain {parsed_full.hostname!r} is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
        )

    # Append the state parameter securely
    query = urllib.parse.urlencode({"state": session_token})
    # Preserve any existing query parameters in the callback path
    if parsed_full.query:
        query = f"{parsed_full.query}&{query}"

    # Reconstruct the final URL
    callback_url = urllib.parse.urlunparse(
        (
            parsed_full.scheme,
            parsed_full.netloc,
            parsed_full.path,
            parsed_full.params,
            query,
            parsed_full.fragment,
        )
    )

    return callback_url