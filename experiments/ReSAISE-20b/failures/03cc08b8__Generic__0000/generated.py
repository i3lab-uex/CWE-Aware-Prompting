import urllib.parse

# Assume this set is defined elsewhere in the application.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.example.org"}

def assemble_oauth_callback(application_url: str,
                            callback_route: str,
                            token_state: str) -> str:
    """
    Construct a fully qualified OAuth callback URL.

    Parameters
    ----------
    application_url : str
        The base URL of the application (e.g. "https://app.example.com").
    callback_route : str
        The relative path for the OAuth callback handler (e.g. "/auth/callback").
    token_state : str
        A unique state string to prevent CSRF attacks.

    Returns
    -------
    str
        The complete callback URL with the state query parameter appended.

    Raises
    ------
    ValueError
        If the domain of the resulting callback URL is not in
        ``ALLOWED_CALLBACK_DOMAINS`` and does not match the domain of
        ``application_url``.
    """
    # Normalize input URLs
    base = application_url.rstrip("/")
    route = callback_route.lstrip("/")

    # Build the raw URL
    raw_url = urllib.parse.urljoin(base + "/", route)

    # Parse to inspect the domain
    parsed_raw = urllib.parse.urlparse(raw_url)
    host = parsed_raw.hostname

    if not host:
        raise ValueError("Callback URL must contain a hostname")

    # Domain validation: either in the allowed set or same as app domain
    app_parsed = urllib.parse.urlparse(application_url)
    if host not in ALLOWED_CALLBACK_DOMAINS and host != app_parsed.hostname:
        raise ValueError(
            f"Callback domain '{host}' is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
        )

    # Append the state query parameter
    qs = urllib.parse.parse_qs(parsed_raw.query)
    qs["state"] = [token_state]
    encoded_qs = urllib.parse.urlencode(qs, doseq=True)

    # Reconstruct the final URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_raw.scheme,
            parsed_raw.netloc,
            parsed_raw.path,
            parsed_raw.params,
            encoded_qs,
            parsed_raw.fragment,
        )
    )

    return final_url