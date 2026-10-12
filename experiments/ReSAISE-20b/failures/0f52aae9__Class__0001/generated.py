import urllib.parse

# Example set of allowed callback domains.  In a real application this would be
# populated from configuration or environment variables.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.myapp.com",
    # Add any additional trusted domains here.
}


def build_oauth_redirect_url(main_url: str, redirect_endpoint: str, session_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The root URL of the application (e.g. "https://myapp.com").
    redirect_endpoint : str
        The endpoint path for the OAuth callback handler (e.g. "/auth/callback").
    session_state : str
        A unique identifier used to maintain the integrity of the OAuth exchange.

    Returns
    -------
    str
        The fully assembled OAuth callback URL with a state query parameter.

    Raises
    ------
    ValueError
        If the callback URL domain is not in ``ALLOWED_CALLBACK_DOMAINS`` and does not
        match the domain of ``main_url``.
    """
    # Resolve the full callback URL by joining the base and endpoint
    raw_callback_url = urllib.parse.urljoin(main_url.rstrip('/') + '/', redirect_endpoint.lstrip('/'))

    # Parse the resulting URL
    parsed = urllib.parse.urlparse(raw_callback_url)

    # Ensure we have a scheme and network location
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid callback URL constructed from inputs")

    # Verify domain: either same as main_url or in the allowed list
    main_parsed = urllib.parse.urlparse(main_url)
    if parsed.netloc != main_parsed.netloc and parsed.hostname not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Callback domain '{parsed.netloc}' is not allowed")

    # Append the state parameter safely
    query_params = dict(urllib.parse.parse_qsl(parsed.query))
    query_params["state"] = session_state
    new_query = urllib.parse.urlencode(query_params)

    # Rebuild the URL with the updated query string
    safe_callback_url = urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))

    return safe_callback_url