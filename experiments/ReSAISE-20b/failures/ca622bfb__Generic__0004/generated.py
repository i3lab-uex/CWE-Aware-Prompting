import urllib.parse

# Example set of allowed domains; in real use this would be defined elsewhere.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add other trusted domains here
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
        The relative path that will handle the OAuth callback (e.g., "/auth/callback").
    session_token : str
        A random token used as the `state` parameter to protect against CSRF.

    Returns
    -------
    str
        The fully qualified callback URL including the `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in
        :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Parse the root URL to ensure it contains scheme and netloc
    parsed_root = urllib.parse.urlparse(root_url)
    if not parsed_root.scheme or not parsed_root.netloc:
        raise ValueError(f"Invalid root URL: {root_url!r}")

    # Join the base and callback path
    joined = urllib.parse.urljoin(root_url.rstrip('/') + '/', path_for_callback.lstrip('/'))

    # Append the state parameter
    url_parts = list(urllib.parse.urlparse(joined))
    query_params = urllib.parse.parse_qs(url_parts[4])
    query_params['state'] = [session_token]
    url_parts[4] = urllib.parse.urlencode(query_params, doseq=True)
    full_url = urllib.parse.urlunparse(url_parts)

    # Validate domain
    callback_domain = urllib.parse.urlparse(full_url).hostname
    if not callback_domain or callback_domain.lower() not in {d.lower() for d in ALLOWED_CALLBACK_DOMAINS}:
        raise ValueError(f"Unauthorized callback domain: {callback_domain!r}")

    return full_url