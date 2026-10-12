import urllib.parse

# Domains that are allowed to receive OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add other trusted domains here.
}


def build_oauth_redirect_url(main_url: str, redirect_path: str, nonce: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        Base URL of the application (e.g. 'https://app.example.com')
    redirect_path : str
        Path to handle the OAuth callback (e.g. '/auth/callback')
    nonce : str
        State value used to prevent CSRF.

    Returns
    -------
    str
        Fully-qualified OAuth callback URL containing the state parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL resolves to a domain that is not in
        ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Parse the main URL to isolate scheme and netloc
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError("`main_url` must be a valid absolute URL")

    # Ensure the redirect path starts with a slash
    if not redirect_path.startswith("/"):
        redirect_path = "/" + redirect_path

    # Join the base URL and path safely
    callback_url = urllib.parse.urljoin(
        f"{parsed_main.scheme}://{parsed_main.netloc}", redirect_path
    )

    # Append the state parameter safely (encoding the nonce)
    query = urllib.parse.urlencode({"state": nonce})
    callback_url_with_state = f"{callback_url}?{query}"

    # Verify the domain is allowed
    parsed_callback = urllib.parse.urlparse(callback_url_with_state)
    host = parsed_callback.hostname or ""
    if host not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Unauthorized callback domain: {host}")

    return callback_url_with_state