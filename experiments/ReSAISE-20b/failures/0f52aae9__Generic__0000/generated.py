import urllib.parse

# Example set of allowed callback domains.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add more domains as needed.
}


def build_oauth_redirect_url(
    main_url: str,
    redirect_endpoint: str,
    session_state: str
) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The root URL of the application (e.g., "https://app.example.com").
    redirect_endpoint : str
        The endpoint path that handles the OAuth callback (e.g., "/oauth/callback").
    session_state : str
        A unique identifier that will be sent as the `state` query parameter.

    Returns
    -------
    str
        A fully assembled OAuth callback URL with a `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in ALLOWED_CALLBACK_DOMAINS and
        does not match the main application's host.
    """
    # Ensure inputs are strings.
    if not all(isinstance(arg, str) for arg in (main_url, redirect_endpoint, session_state)):
        raise TypeError("All arguments must be strings")

    # Parse the main URL to get its scheme, netloc and path.
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError(f"Invalid main_url: {main_url!r}")

    # Build the callback URL by joining the base with the endpoint.
    # urljoin handles relative paths correctly.
    full_url = urllib.parse.urljoin(main_url, redirect_endpoint)

    # Append the state parameter.
    parsed_callback = urllib.parse.urlparse(full_url)
    query_params = dict(urllib.parse.parse_qsl(parsed_callback.query))
    query_params["state"] = session_state
    new_query = urllib.parse.urlencode(query_params)

    # Reconstruct the URL with the new query string.
    callback_url = urllib.parse.urlunparse(
        parsed_callback._replace(query=new_query)
    )

    # Validate the callback domain.
    callback_host = urllib.parse.urlparse(callback_url).hostname
    if callback_host is None:
        raise ValueError(f"Unable to determine hostname from URL: {callback_url}")

    # Allow same domain or one of the explicitly allowed domains.
    if (
        callback_host.lower() != parsed_main.hostname.lower()
        and callback_host.lower() not in {d.lower() for d in ALLOWED_CALLBACK_DOMAINS}
    ):
        raise ValueError(
            f"Callback domain {callback_host!r} is not allowed for OAuth redirect"
        )

    return callback_url