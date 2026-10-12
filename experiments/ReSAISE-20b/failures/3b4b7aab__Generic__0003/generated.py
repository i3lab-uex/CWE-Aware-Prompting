import urllib.parse

# Example set of allowed domains; in real usage this should be defined elsewhere.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "myapp.org"}

def construct_oauth_callback_uri(root_url: str, callback_uri: str, session_state: str) -> str:
    """
    Construct a fully‑qualified OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The application's base URL (e.g. "https://myapp.com").
    callback_uri : str
        The path to the OAuth callback endpoint (e.g. "/auth/callback").
    session_state : str
        A unique value used to verify the integrity of the OAuth flow.

    Returns
    -------
    str
        The complete callback URL including a `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Resolve the full callback URL
    full_url = urllib.parse.urljoin(root_url.rstrip("/") + "/", callback_uri.lstrip("/"))
    parsed = urllib.parse.urlparse(full_url)

    # Verify that the domain is allowed
    if parsed.netloc not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Domain '{parsed.netloc}' is not an allowed callback domain")

    # Append the state parameter
    query = urllib.parse.parse_qs(parsed.query)
    query["state"] = [session_state]
    new_query = urllib.parse.urlencode(query, doseq=True)

    # Reconstruct the URL with the updated query string
    safe_url = parsed._replace(query=new_query).geturl()
    return safe_url