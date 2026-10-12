import urllib.parse

# Example allowed domains; adjust as needed for your application.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
}

def build_oauth_redirect_url(main_url: str, redirect_path: str, token_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The application's base URL (e.g., "https://app.example.com").
    redirect_path : str
        The specific path for the OAuth callback endpoint (e.g., "/auth/callback").
    token_state : str
        A unique value to include as a query parameter for state validation.

    Returns
    -------
    str
        The fully-qualified OAuth callback URL.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Parse the main URL and ensure it has a scheme
    base = urllib.parse.urlparse(main_url)
    if not base.scheme:
        raise ValueError(f"Main URL must include a scheme: {main_url!r}")

    # Join the path safely
    joined_path = urllib.parse.urljoin(base.path + "/", redirect_path.lstrip("/"))

    # Build query parameters, ensuring 'state' is the only parameter
    query = urllib.parse.urlencode({"state": token_state})

    # Reconstruct the full URL
    new_url = urllib.parse.urlunparse(
        (
            base.scheme,
            base.netloc,
            joined_path,
            "",  # params
            query,
            "",  # fragment
        )
    )

    # Validate the domain against allowed domains
    domain = urllib.parse.urlparse(new_url).netloc.split(":")[0]  # strip port if present
    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Disallowed callback domain: {domain!r}")

    return new_url