import urllib.parse

# Example set of allowed callback domains. In a real application this should be
# defined in configuration or environment variables.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
}

def build_oauth_redirect_url(main_url: str, redirect_path: str, nonce: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        Base URL of the application (e.g. "https://app.example.com").
    redirect_path : str
        Path that will handle the OAuth callback (e.g. "/auth/callback").
    nonce : str
        A cryptographically random string used as the state parameter.

    Returns
    -------
    str
        The full callback URL with the `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in ALLOWED_CALLBACK_DOMAINS.
    """
    # Validate and normalize the main URL
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError(f"Invalid main URL: {main_url!r}")

    # Ensure redirect_path starts with a slash
    if not redirect_path.startswith("/"):
        redirect_path = "/" + redirect_path

    # Join the base URL with the callback path
    joined_url = urllib.parse.urljoin(main_url, redirect_path)

    # Append the state (nonce) as a query parameter
    query = urllib.parse.urlencode({"state": nonce})
    full_url = f"{joined_url}?{query}"

    # Verify that the domain is allowed
    parsed_full = urllib.parse.urlparse(full_url)
    domain = parsed_full.hostname
    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Unauthorized callback domain: {domain!r}")

    return full_url