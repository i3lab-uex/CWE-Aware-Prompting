import urllib.parse

# Example set of allowed domains for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    "localhost",
}

def assemble_oauth_callback(application_url: str, callback_route: str,
                            token_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    application_url : str
        The base URL of the application (e.g. "https://app.example.com").
    callback_route : str
        The relative route to the OAuth callback handler (e.g. "/oauth/callback").
    token_state : str
        A unique identifier that should be preserved across the OAuth flow.

    Returns
    -------
    str
        The fully assembled callback URL including a `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in `ALLOWED_CALLBACK_DOMAINS`
        or does not match the application's domain.
    """
    # Normalize and parse the application URL
    app_parsed = urllib.parse.urlparse(application_url)
    if not app_parsed.scheme or not app_parsed.netloc:
        raise ValueError(f"Invalid application_url: {application_url!r}")

    # Join the callback route with the base URL
    full_callback = urllib.parse.urljoin(application_url, callback_route)

    # Parse the resulting URL to inspect its components
    cb_parsed = urllib.parse.urlparse(full_callback)

    # Determine the domain of the callback URL
    cb_domain = cb_parsed.hostname
    if not cb_domain:
        raise ValueError(f"Callback URL has no hostname: {full_callback!r}")

    # Check domain restrictions
    app_domain = app_parsed.hostname
    if cb_domain != app_domain and cb_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Disallowed callback domain: {cb_domain!r}. "
            f"Allowed domains are {sorted(ALLOWED_CALLBACK_DOMAINS)}."
        )

    # Append the state parameter safely
    query = urllib.parse.parse_qs(cb_parsed.query, keep_blank_values=True)
    # `parse_qs` returns values as lists; we need a single value
    query["state"] = [token_state]
    encoded_query = urllib.parse.urlencode(query, doseq=True)

    # Reconstruct the final URL
    assembled = urllib.parse.urlunparse(
        (
            cb_parsed.scheme,
            cb_parsed.netloc,
            cb_parsed.path,
            cb_parsed.params,
            encoded_query,
            cb_parsed.fragment,
        )
    )

    return assembled