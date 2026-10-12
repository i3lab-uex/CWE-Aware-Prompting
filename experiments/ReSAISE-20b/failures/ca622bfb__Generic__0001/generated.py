import urllib.parse

# Example set of allowed domains; in a real app this would be configured elsewhere.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.example.org"}

def assemble_oauth_callback_url(
    root_url: str,
    path_for_callback: str,
    session_token: str
) -> str:
    """
    Build a full OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The base URL of the application (e.g. "https://app.example.com").
    path_for_callback : str
        The relative path that handles the OAuth callback (e.g. "/auth/callback").
    session_token : str
        A unique token used as the `state` query parameter to protect against CSRF.

    Returns
    -------
    str
        The fully-qualified callback URL with the `state` query parameter appended.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to an allowed domain or if the
        root_url is missing a scheme.
    """
    # Ensure root URL has a scheme; otherwise urljoin will treat it as a path.
    parsed_root = urllib.parse.urlparse(root_url)
    if not parsed_root.scheme:
        raise ValueError(f"Root URL must include a scheme (http/https): {root_url}")

    # Join root and path to form the base callback URL
    base_callback = urllib.parse.urljoin(root_url, path_for_callback)

    # Validate the domain
    parsed_base = urllib.parse.urlparse(base_callback)
    if not parsed_base.netloc:
        raise ValueError(f"Invalid callback URL: {base_callback}")

    domain = parsed_base.netloc.split(':')[0]  # strip port if present
    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not allowed for OAuth callbacks")

    # Append the state parameter
    query = urllib.parse.urlencode({"state": session_token})
    callback_url = f"{base_callback}?{query}"

    return callback_url