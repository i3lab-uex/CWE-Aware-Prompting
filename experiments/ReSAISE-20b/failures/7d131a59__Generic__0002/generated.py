import urllib.parse

# Example set of allowed callback domains.  In a real application, this would be
# populated from configuration or environment variables.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    "myapp.localhost",
}

def create_oauth_callback_url(base_url: str, callback_path: str, state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    base_url : str
        The base URL of the application (e.g., "https://myapp.com").
    callback_path : str
        The path to append to the base URL for the OAuth callback
        (e.g., "/oauth/callback").
    state : str
        A unique opaque value to be sent back by the OAuth provider.

    Returns
    -------
    str
        The fully-qualified callback URL including the `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to a domain listed in
        ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Build the raw URL without query parameters
    raw_url = urllib.parse.urljoin(base_url.rstrip('/') + '/', callback_path.lstrip('/'))

    # Parse the URL to inspect its components
    parsed = urllib.parse.urlparse(raw_url)

    # Validate the domain against allowed list (case-insensitive)
    hostname = parsed.hostname
    if not hostname or hostname.lower() not in {d.lower() for d in ALLOWED_CALLBACK_DOMAINS}:
        raise ValueError(f"Disallowed callback domain: {hostname!r}")

    # Append the state parameter safely
    query_params = urllib.parse.parse_qs(parsed.query)
    query_params["state"] = [state]
    encoded_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the full URL with encoded query string
    final_url = urllib.parse.urlunparse(
        parsed._replace(query=encoded_query)
    )

    return final_url