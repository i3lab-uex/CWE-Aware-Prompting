import urllib.parse

# Domains that are considered safe for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    "localhost:8000",
}

def build_oauth_redirect_url(main_url: str, redirect_path: str, token_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The application's base URL (e.g., "https://app.example.com").
    redirect_path : str
        The relative path for the OAuth callback (e.g., "/auth/callback").
    token_state : str
        A unique value to be sent as a query parameter for state verification.

    Returns
    -------
    str
        A fully qualified URL ready to be used as the OAuth redirect URI.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Ensure the base URL has a scheme
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme:
        raise ValueError("Base URL must include a scheme (e.g., 'https://').")

    # Resolve the full path relative to the base URL
    joined = urllib.parse.urljoin(main_url, redirect_path)

    # Parse the resulting URL to extract components
    parsed = urllib.parse.urlparse(joined)

    # Verify domain (netloc) against allowed list
    if parsed.netloc not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain '{parsed.netloc}' is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
        )

    # Append the state parameter securely
    query = urllib.parse.urlencode({"state": token_state})
    # Rebuild the URL with the new query string
    final_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            query,
            parsed.fragment,
        )
    )

    return final_url