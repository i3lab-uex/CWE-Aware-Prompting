import urllib.parse

# Example allowed domains; replace with your actual policy.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.myapp.org"}


def generate_oauth_url(host_url: str, path_callback: str, session_id: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    host_url : str
        The base URL of the application (e.g. "https://app.example.com").
    path_callback : str
        The endpoint that will handle the OAuth callback (e.g. "/auth/callback").
    session_id : str
        A unique identifier used as the `state` query parameter.

    Returns
    -------
    str
        The fully assembled OAuth callback URL.

    Raises
    ------
    ValueError
        If the resulting domain is not in ALLOWED_CALLBACK_DOMAINS or does not match
        the host's domain.
    """
    if not isinstance(host_url, str) or not isinstance(path_callback, str) or not isinstance(session_id, str):
        raise TypeError("All arguments must be strings")

    # Ensure path_callback starts with a slash
    if not path_callback.startswith("/"):
        path_callback = "/" + path_callback

    # Build the full callback URL
    base_parsed = urllib.parse.urlparse(host_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Invalid host_url: {host_url}")

    # Resolve the callback path against the base URL
    full_path = urllib.parse.urljoin(host_url, path_callback)

    # Parse the resulting URL to inspect its components
    full_parsed = urllib.parse.urlparse(full_path)

    # Validate domain: either same as host or in allowed list
    callback_domain = full_parsed.hostname
    if callback_domain is None:
        raise ValueError(f"Callback URL has no hostname: {full_path}")

    host_domain = base_parsed.hostname
    if callback_domain != host_domain and callback_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain '{callback_domain}' is not allowed. "
            f"Allowed domains: {ALLOWED_CALLBACK_DOMAINS}"
        )

    # Append the state parameter securely
    query = urllib.parse.parse_qs(full_parsed.query)
    query["state"] = [session_id]
    encoded_query = urllib.parse.urlencode(query, doseq=True)

    # Reconstruct the full URL with the new query string
    final_url = urllib.parse.urlunparse(
        (
            full_parsed.scheme,
            full_parsed.netloc,
            full_parsed.path,
            full_parsed.params,
            encoded_query,
            full_parsed.fragment,
        )
    )

    return final_url