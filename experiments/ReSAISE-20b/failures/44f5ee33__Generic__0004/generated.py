import urllib.parse

# Domains that are allowed for OAuth callback URLs.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    "localhost",
    # Add other authorized domains here.
}


def build_oauth_redirect_url(main_url: str, redirect_path: str, nonce: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g. "https://app.example.com").
    redirect_path : str
        The path that handles the OAuth callback (e.g. "/oauth/callback").
    nonce : str
        A random string used as the state parameter for CSRF protection.

    Returns
    -------
    str
        The fully qualified callback URL including the state query parameter.

    Raises
    ------
    ValueError
        If the domain of `main_url` is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Parse the main URL and validate its domain.
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError(f"Invalid main URL: {main_url!r}")

    domain = parsed_main.hostname.lower()
    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not authorized for OAuth callbacks")

    # Ensure redirect_path starts with a slash.
    if not redirect_path.startswith("/"):
        redirect_path = "/" + redirect_path

    # Build the path by joining base path with redirect_path.
    base_path = parsed_main.path
    if not base_path.endswith("/"):
        base_path += "/"
    full_path = urllib.parse.urljoin(base_path, redirect_path.lstrip("/"))

    # Append the state query parameter.
    query = urllib.parse.urlencode({"state": nonce})
    callback_url_parts = (
        parsed_main.scheme,
        parsed_main.netloc,
        full_path,
        "",  # params
        query,
        ""   # fragment
    )
    callback_url = urllib.parse.urlunparse(callback_url_parts)

    return callback_url