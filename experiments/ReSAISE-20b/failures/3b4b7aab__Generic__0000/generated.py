import urllib.parse

# Example list of allowed callback domains. In a real application this would be configured elsewhere.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    "localhost:8000",  # for local development
}

def construct_oauth_callback_uri(root_url: str, callback_uri: str, session_state: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The application's main base URL (e.g., "https://myapp.com").
    callback_uri : str
        The specific path for the OAuth callback endpoint (e.g., "/auth/callback").
    session_state : str
        A unique value used to verify the integrity of the OAuth flow.

    Returns
    -------
    str
        The fully constructed callback URL with a ``state`` query parameter.

    Raises
    ------
    ValueError
        If the domain of the resulting URL is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Normalise the root URL (ensure scheme is present)
    parsed_root = urllib.parse.urlparse(root_url)
    if not parsed_root.scheme:
        raise ValueError("root_url must include a scheme (http:// or https://)")

    # Join the root URL with the callback path
    full_url = urllib.parse.urljoin(root_url, callback_uri)

    # Parse the URL to manipulate query parameters
    parsed = urllib.parse.urlparse(full_url)
    qs = dict(urllib.parse.parse_qsl(parsed.query, keep_blank_values=True))
    qs["state"] = session_state

    # Rebuild the URL with updated query string
    new_query = urllib.parse.urlencode(qs)
    final_url = parsed._replace(query=new_query).geturl()

    # Validate the domain
    netloc = urllib.parse.urlparse(final_url).netloc.lower()
    if netloc not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Disallowed callback domain: {netloc}")

    return final_url