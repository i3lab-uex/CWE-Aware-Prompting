import urllib.parse

# Example set of domains that are considered safe for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    "localhost",
}

def generate_oauth_callback_link(
    app_base_url: str,
    callback_endpoint: str,
    verification_state: str
) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The application's main base URL (e.g., "https://app.example.com").
    callback_endpoint : str
        The specific path for the OAuth callback endpoint (e.g., "/auth/callback").
    verification_state : str
        A unique value to include as a query parameter for state verification.

    Returns
    -------
    str
        The fully-qualified OAuth callback URL.

    Raises
    ------
    ValueError
        If the resulting callback URL resolves to a domain not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Ensure the base URL has a scheme; default to https if missing
    parsed_base = urllib.parse.urlparse(app_base_url)
    if not parsed_base.scheme:
        app_base_url = f"https://{app_base_url}"
        parsed_base = urllib.parse.urlparse(app_base_url)

    # Construct the full callback URL using urljoin to correctly handle relative paths
    joined = urllib.parse.urljoin(app_base_url, callback_endpoint)

    # Append the state parameter
    query = urllib.parse.urlencode({"state": verification_state})
    callback_url = f"{joined}?{query}"

    # Validate the domain of the resulting URL
    parsed_callback = urllib.parse.urlparse(callback_url)
    # Normalise domain: strip port, convert to lowercase
    netloc = parsed_callback.hostname or ""
    if netloc.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Disallowed callback domain: '{netloc}'. Allowed domains are: "
            f"{', '.join(sorted(ALLOWED_CALLBACK_DOMAINS))}"
        )

    return callback_url