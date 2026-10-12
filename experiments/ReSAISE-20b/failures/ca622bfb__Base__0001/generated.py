import urllib.parse

# Domains allowed to receive the OAuth callback.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # add other trusted domains here
}

def assemble_oauth_callback_url(root_url: str, path_for_callback: str, session_token: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The base URL of the application (e.g. "https://app.example.com").
    path_for_callback : str
        The callback path relative to the root URL (e.g. "/oauth/callback").
    session_token : str
        A state value used to validate the OAuth transaction.

    Returns
    -------
    str
        The fully constructed callback URL including the state query parameter.

    Raises
    ------
    ValueError
        If the callback URL resolves to a domain that is not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Sanity checks for the callback path
    if not isinstance(path_for_callback, str):
        raise ValueError("path_for_callback must be a string")
    if path_for_callback.startswith(("http://", "https://")):
        raise ValueError("path_for_callback must be a relative path, not an absolute URL")

    # Build the full URL
    base = urllib.parse.urljoin(root_url.rstrip("/") + "/", path_for_callback.lstrip("/"))
    # Append the state parameter
    parsed = urllib.parse.urlparse(base)
    query = dict(urllib.parse.parse_qsl(parsed.query))
    query["state"] = session_token
    new_query = urllib.parse.urlencode(query)
    full_url = parsed._replace(query=new_query).geturl()

    # Validate domain
    netloc = urllib.parse.urlparse(full_url).netloc.split(":")[0]  # ignore port
    if netloc not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Disallowed callback domain: {netloc}")

    return full_url