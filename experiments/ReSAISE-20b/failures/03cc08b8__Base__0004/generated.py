import urllib.parse

# Example set of allowed domains for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    "myapp.local",
}

def assemble_oauth_callback(application_url: str,
                            callback_route: str,
                            token_state: str) -> str:
    """
    Assemble a secure OAuth callback URL.

    Parameters
    ----------
    application_url : str
        The base URL of the application (e.g. "https://app.example.com").
    callback_route : str
        The path for the OAuth callback handler (e.g. "/oauth/callback").
    token_state : str
        A unique identifier to maintain the integrity of the OAuth exchange.

    Returns
    -------
    str
        The fully assembled callback URL with state appended as a query
        parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in
        ``ALLOWED_CALLBACK_DOMAINS`` and does not match the host of
        ``application_url``.
    """
    # Parse base application URL and callback route
    base_parsed = urllib.parse.urlparse(application_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("Invalid application_url: missing scheme or host")

    # Ensure callback_route starts with a slash
    route = callback_route if callback_route.startswith("/") else f"/{callback_route}"
    # Construct the full path
    combined_path = urllib.parse.urljoin(base_parsed.path, route)

    # Build the new URL components
    callback_url_parts = (
        base_parsed.scheme,
        base_parsed.netloc,
        combined_path,
        "",  # params
        urllib.parse.urlencode({"state": token_state}),
        ""   # fragment
    )
    callback_url = urllib.parse.urlunparse(callback_url_parts)

    # Validate the domain
    parsed_callback = urllib.parse.urlparse(callback_url)
    callback_domain = parsed_callback.hostname

    if not callback_domain:
        raise ValueError("Callback URL has no hostname")

    # Allow the domain if it matches application host or is in the allowed list
    if (callback_domain != base_parsed.hostname and
            callback_domain not in ALLOWED_CALLBACK_DOMAINS):
        raise ValueError(
            f"Disallowed callback domain: {callback_domain!r}. "
            "Must be same as application host or in ALLOWED_CALLBACK_DOMAINS."
        )

    return callback_url