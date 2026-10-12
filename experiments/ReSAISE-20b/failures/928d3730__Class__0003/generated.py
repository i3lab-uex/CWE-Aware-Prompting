import urllib.parse

# Allowed domains for OAuth callbacks – adjust as needed.
ALLOWED_CALLBACK_DOMAINS = {
    "auth.example.com",
    "oauth.partner.com",
}

def generate_oauth_url(host_url: str, path_callback: str, session_id: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    host_url : str
        The base application URL (e.g., "https://app.example.com").
    path_callback : str
        The relative endpoint for the OAuth callback handler (e.g., "/auth/callback").
    session_id : str
        A unique identifier used as the OAuth state parameter.

    Returns
    -------
    str
        The fully assembled callback URL including a `state` query parameter.

    Raises
    ------
    ValueError
        If the resolved callback URL's domain is not in ``ALLOWED_CALLBACK_DOMAINS``
        and does not match the host's domain.
    """
    # Ensure path_callback starts with a slash for urljoin to work correctly
    if not path_callback.startswith("/"):
        path_callback = "/" + path_callback

    # Join the host URL with the callback path
    full_url = urllib.parse.urljoin(host_url.rstrip("/") + "/", path_callback.lstrip("/"))

    # Parse the resulting URL to inspect its components
    parsed = urllib.parse.urlparse(full_url)

    # Extract the hostname (without port) for validation
    callback_hostname = parsed.hostname
    if not callback_hostname:
        raise ValueError("Invalid callback URL: missing hostname")

    # Validate the domain against allowed domains or same as host
    host_parsed = urllib.parse.urlparse(host_url)
    host_hostname = host_parsed.hostname
    if (
        callback_hostname not in ALLOWED_CALLBACK_DOMAINS
        and callback_hostname != host_hostname
    ):
        raise ValueError(
            f"Callback domain '{callback_hostname}' is not allowed for OAuth redirects"
        )

    # Append the state parameter safely (preserving existing query parameters)
    query_params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    query_params["state"] = [session_id]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the final URL
    final_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment,
        )
    )

    return final_url