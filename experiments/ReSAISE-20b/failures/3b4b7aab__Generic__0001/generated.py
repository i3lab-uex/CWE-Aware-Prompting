import urllib.parse

# Example list of allowed callback domains.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    "localhost",  # for local testing
}

def construct_oauth_callback_uri(root_url: str, callback_uri: str, session_state: str) -> str:
    """
    Build a full OAuth callback URL and ensure its domain is allowed.

    Parameters
    ----------
    root_url : str
        The base URL of the application, e.g. "https://app.example.com".
    callback_uri : str
        The relative path to the OAuth callback endpoint, e.g. "/auth/callback".
    session_state : str
        A unique value that will be sent back as a query parameter to verify the OAuth flow.

    Returns
    -------
    str
        The fully qualified callback URL with `state` query parameter appended.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Build the base callback URL
    full_url = urllib.parse.urljoin(root_url, callback_uri)

    # Parse the URL to inspect its components
    parsed = urllib.parse.urlparse(full_url)

    # Extract hostname and verify against allowed domains
    hostname = parsed.hostname or ""
    if hostname.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Disallowed callback domain: {hostname}")

    # Append the state parameter safely
    query_params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    query_params["state"] = [session_state]

    # Reconstruct the URL with updated query string
    new_query = urllib.parse.urlencode(query_params, doseq=True)
    safe_url = parsed._replace(query=new_query).geturl()

    return safe_url