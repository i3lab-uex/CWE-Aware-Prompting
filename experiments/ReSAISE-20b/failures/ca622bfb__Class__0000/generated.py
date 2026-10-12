import urllib.parse

# Example set of allowed callback domains – replace with your real values.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.myapp.com"}


def assemble_oauth_callback_url(root_url: str, path_for_callback: str, session_token: str) -> str:
    """
    Build a fully-qualified OAuth callback URL that includes the state parameter.

    Parameters
    ----------
    root_url : str
        The base URL of the application (e.g., "https://myapp.com").
    path_for_callback : str
        The relative path that should handle the OAuth callback (e.g., "/auth/callback").
    session_token : str
        A token used as the state parameter to protect against CSRF.

    Returns
    -------
    str
        The full callback URL including the `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Ensure root_url is a proper absolute URL.
    parsed_root = urllib.parse.urlparse(root_url)
    if not parsed_root.scheme or not parsed_root.netloc:
        raise ValueError(f"root_url must be a valid absolute URL, got: {root_url!r}")

    # Build the path part of the callback.
    # `urljoin` handles leading/trailing slashes correctly.
    callback_path = urllib.parse.urljoin(parsed_root.path, path_for_callback)

    # Construct the query string with the state parameter.
    query = urllib.parse.urlencode({"state": session_token})

    # Assemble the full URL components.
    callback_url = urllib.parse.urlunparse(
        (
            parsed_root.scheme,
            parsed_root.netloc,
            callback_path,
            "",  # params
            query,
            "",  # fragment
        )
    )

    # Validate the domain against allowed callback domains.
    parsed_callback = urllib.parse.urlparse(callback_url)
    domain = parsed_callback.hostname
    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Unauthorized callback domain: {domain!r}. "
            f"Allowed domains are: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
        )

    return callback_url