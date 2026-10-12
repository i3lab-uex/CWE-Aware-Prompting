import urllib.parse

# Domains that are allowed to receive OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "sub.example.org",
}

def assemble_oauth_callback_url(root_url: str, path_for_callback: str, session_token: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The base URL of the application (e.g. "https://myapp.com").
    path_for_callback : str
        The path to the callback endpoint (e.g. "/auth/callback").
    session_token : str
        A unique token used as the state parameter.

    Returns
    -------
    str
        The fully-qualified callback URL including the `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting URL points to a domain that is not in
        :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Ensure the callback path starts with a slash
    if not path_for_callback.startswith("/"):
        raise ValueError("callback path must start with '/'")

    # Combine the root URL and callback path
    base = urllib.parse.urljoin(root_url.rstrip("/") + "/", path_for_callback.lstrip("/"))

    # Parse the combined URL to extract its components
    parsed = urllib.parse.urlparse(base)

    # Validate that the domain is allowed
    host = parsed.hostname or ""
    if host not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Domain '{host}' is not authorized for OAuth callbacks")

    # Append the state parameter
    query = urllib.parse.urlencode({"state": session_token})
    callback_url = urllib.parse.urlunparse(
        parsed._replace(query=query)
    )

    return callback_url