import urllib.parse

# Example set of allowed callback domains. In real usage this should be defined elsewhere
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
}

def build_oauth_redirect_url(main_url: str, redirect_endpoint: str, session_state: str) -> str:
    """
    Build a fully-qualified OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The root URL of the application (e.g. "https://app.example.com").
    redirect_endpoint : str
        The endpoint path for the OAuth callback handler (e.g. "/oauth/callback").
    session_state : str
        A unique identifier used to maintain state during the OAuth exchange.

    Returns
    -------
    str
        A fully assembled URL that includes the callback path and a `state` query parameter.

    Raises
    ------
    ValueError
        If the domain of the constructed callback URL is not in ``ALLOWED_CALLBACK_DOMAINS``
        or does not match the domain of ``main_url``.
    """
    # Ensure inputs are strings
    if not all(isinstance(arg, str) for arg in (main_url, redirect_endpoint, session_state)):
        raise TypeError("All arguments must be strings")

    # Normalise the main URL
    parsed_main = urllib.parse.urlparse(main_url.rstrip("/"))
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError(f"Invalid main_url: {main_url!r}")

    # Build the base callback URL
    base_callback = urllib.parse.urljoin(parsed_main.geturl() + "/", redirect_endpoint.lstrip("/"))

    # Validate the domain of the callback URL
    parsed_callback = urllib.parse.urlparse(base_callback)
    callback_domain = parsed_callback.hostname

    if callback_domain is None:
        raise ValueError(f"Could not determine hostname from callback URL: {base_callback!r}")

    # Domain must either match the main domain or be explicitly allowed
    if callback_domain != parsed_main.hostname and callback_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain {callback_domain!r} is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
        )

    # Append the state parameter
    query = urllib.parse.urlencode({"state": session_state})
    final_url = f"{base_callback}?{query}"

    return final_url