import urllib.parse

# Example set of allowed callback domains; replace with real values as needed.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
}

def build_oauth_redirect_url(main_url: str, redirect_endpoint: str, session_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g., "https://app.example.com").
    redirect_endpoint : str
        The endpoint path for the OAuth callback (e.g., "/auth/callback").
    session_state : str
        A unique identifier for the OAuth exchange.

    Returns
    -------
    str
        The fully assembled callback URL including a state query parameter.

    Raises
    ------
    ValueError
        If the resulting callback domain is not in ALLOWED_CALLBACK_DOMAINS or does not match
        the domain of main_url.
    """
    # Parse the base URL and ensure it has a scheme
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme:
        raise ValueError("main_url must include a scheme (e.g., https://)")

    # Build the full callback URL by joining the base and endpoint
    joined = urllib.parse.urljoin(parsed_main.geturl(), redirect_endpoint)

    # Parse the resulting URL to inspect its components
    parsed_callback = urllib.parse.urlparse(joined)

    # Extract host without port and compare with allowed domains
    host = parsed_callback.hostname
    if not host:
        raise ValueError("Callback URL does not contain a valid hostname")

    # Check domain restrictions
    if host not in ALLOWED_CALLBACK_DOMAINS and host != parsed_main.hostname:
        raise ValueError(f"Callback domain '{host}' is not allowed")

    # Build query string with the state parameter
    query = urllib.parse.urlencode({"state": session_state})

    # Reconstruct the full URL with the query string
    callback_url = urllib.parse.urlunparse(
        (
            parsed_callback.scheme,
            parsed_callback.netloc,
            parsed_callback.path,
            parsed_callback.params,
            query,
            parsed_callback.fragment,
        )
    )

    return callback_url