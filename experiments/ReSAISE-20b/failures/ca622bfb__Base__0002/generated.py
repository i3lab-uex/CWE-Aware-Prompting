import urllib.parse

# Example set of allowed domains for the OAuth callback.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.example.org"}

def assemble_oauth_callback_url(
    root_url: str,
    path_for_callback: str,
    session_token: str
) -> str:
    """
    Build a fully qualified OAuth callback URL and ensure it points to an
    authorized domain.

    Parameters
    ----------
    root_url : str
        The base URL of the application (e.g., "https://myapp.com").
    path_for_callback : str
        The callback path (e.g., "/auth/oauth/callback").
    session_token : str
        A token used as the `state` query parameter to protect against CSRF.

    Returns
    -------
    str
        The complete OAuth callback URL with the state query parameter.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in
        `ALLOWED_CALLBACK_DOMAINS`.
    """
    # Normalize the root URL and path, then join them.
    base = urllib.parse.urljoin(root_url.rstrip("/") + "/", path_for_callback.lstrip("/"))

    # Parse the resulting URL to inspect its components.
    parsed = urllib.parse.urlparse(base)

    # Ensure we are using HTTPS for security.
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Callback URL must use http or https scheme")

    # Validate the domain against the whitelist.
    hostname = parsed.hostname
    if not hostname or hostname.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Unauthorized callback domain: {hostname}")

    # Add the state parameter to the query string.
    query = urllib.parse.parse_qs(parsed.query)
    query["state"] = [session_token]
    encoded_query = urllib.parse.urlencode(query, doseq=True)

    # Rebuild the URL with the updated query.
    callback_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            encoded_query,
            parsed.fragment,
        )
    )

    return callback_url