import urllib.parse

# Domains allowed for OAuth callbacks (example set)
ALLOWED_CALLBACK_DOMAINS = {
    "auth.example.com",
    "oauth.example.org",
}

def build_oauth_redirect_url(main_url: str, redirect_path: str, nonce: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g., "https://app.example.com").
    redirect_path : str
        The path that will handle the OAuth callback (e.g., "/auth/callback").
    nonce : str
        A unique state value used to protect against CSRF.

    Returns
    -------
    str
        The fully-qualified OAuth callback URL including the state query param.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Parse the base URL to get scheme and netloc
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError(f"Invalid main_url: {main_url!r}")

    # Construct the full URL by joining the path
    joined_path = urllib.parse.urljoin(parsed_main.path + '/', redirect_path.lstrip('/'))
    callback_url = urllib.parse.urlunparse((
        parsed_main.scheme,
        parsed_main.netloc,
        joined_path,
        '',  # params
        urllib.parse.urlencode({'state': nonce}),
        ''   # fragment
    ))

    # Validate domain against allowed list
    callback_netloc = urllib.parse.urlparse(callback_url).netloc.split(':')[0]  # strip port
    if callback_netloc not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Disallowed callback domain: {callback_netloc!r}")

    return callback_url