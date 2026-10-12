import urllib.parse

# Example allowed callback domains – adjust as required for your environment.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
}

def generate_oauth_url(host_url: str, path_callback: str, session_id: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    host_url : str
        The root URL of the application (e.g. "https://app.example.com").
    path_callback : str
        The endpoint for the OAuth callback handler (e.g. "/auth/callback").
    session_id : str
        A unique identifier used to maintain the integrity of the OAuth exchange.

    Returns
    -------
    str
        A fully assembled, validated OAuth callback URL containing a `state`
        query parameter equal to ``session_id``.

    Raises
    ------
    ValueError
        If the resolved callback URL's domain is not within ``ALLOWED_CALLBACK_DOMAINS``
        or does not match the host's domain.
    """
    # Ensure both inputs are strings
    if not all(isinstance(v, str) for v in (host_url, path_callback, session_id)):
        raise TypeError("All arguments must be strings")

    # Normalize the base host URL
    parsed_host = urllib.parse.urlparse(host_url)
    if not parsed_host.scheme or not parsed_host.netloc:
        raise ValueError(f"Invalid host URL: {host_url}")

    # Construct the full callback URL
    joined = urllib.parse.urljoin(host_url, path_callback)
    parsed_joined = urllib.parse.urlparse(joined)

    # Validate that the callback domain is allowed
    host_domain = parsed_host.hostname.lower() if parsed_host.hostname else ""
    callback_domain = parsed_joined.hostname.lower() if parsed_joined.hostname else ""

    # Domain must match host or be in the allowed set
    if callback_domain != host_domain and callback_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain '{callback_domain}' is not allowed. "
            f"Allowed domains: {ALLOWED_CALLBACK_DOMAINS}"
        )

    # Append the state query parameter securely
    query = urllib.parse.parse_qs(parsed_joined.query, keep_blank_values=True)
    query["state"] = [session_id]
    encoded_query = urllib.parse.urlencode(query, doseq=True)

    # Rebuild the final URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_joined.scheme,
            parsed_joined.netloc,
            parsed_joined.path,
            parsed_joined.params,
            encoded_query,
            parsed_joined.fragment,
        )
    )

    return final_url