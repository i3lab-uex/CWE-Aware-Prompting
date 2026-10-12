import urllib.parse

# Domains that are allowed to receive OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add any other domains that are considered safe for callbacks.
}


def build_oauth_redirect_url(main_url: str, redirect_path: str, nonce: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g., "https://myapp.com").
    redirect_path : str
        The path to handle OAuth callbacks (e.g., "/auth/callback").
    nonce : str
        A random string that will be passed as the ``state`` query parameter.

    Returns
    -------
    str
        The fully-qualified callback URL including the ``state`` parameter.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in
        ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Combine the base URL with the callback path safely.
    full_url = urllib.parse.urljoin(main_url.rstrip('/') + '/', redirect_path.lstrip('/'))

    # Parse the URL to inspect its components.
    parsed = urllib.parse.urlparse(full_url)

    # Ensure that the URL uses a safe scheme.
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Invalid URL scheme: {parsed.scheme}")

    # Extract the domain part (netloc may contain port; strip it).
    host = parsed.hostname
    if not host:
        raise ValueError("Callback URL must contain a hostname")

    # Validate the domain against the allowed list.
    if host.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Domain '{host}' is not authorized for OAuth callbacks")

    # Append the nonce as a state parameter.
    query_params = urllib.parse.parse_qs(parsed.query)
    # parse_qs returns lists; we replace or add the state value.
    query_params["state"] = [nonce]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the URL with the new query string.
    safe_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment,
        )
    )

    return safe_url