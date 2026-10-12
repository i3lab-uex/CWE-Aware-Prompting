import urllib.parse

# Example set of allowed callback domains; in a real application this would be configured elsewhere.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.example.org"}

def assemble_oauth_callback_url(root_url: str, path_for_callback: str, session_token: str) -> str:
    """
    Build a full OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The base URL of the application (e.g. "https://app.example.com").
    path_for_callback : str
        The relative path that will handle the OAuth callback (e.g. "/oauth/callback").
    session_token : str
        A token used as a state parameter to protect against CSRF attacks.

    Returns
    -------
    str
        The fully assembled callback URL, including the state query parameter.

    Raises
    ------
    ValueError
        If the resulting URL points to a domain that is not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Normalise root_url to ensure it ends with a slash for correct urljoin behaviour.
    if not root_url.endswith("/"):
        root_url = root_url + "/"

    # Prevent path traversal by rejecting paths that start with '../' or contain '..'
    if ".." in urllib.parse.unquote(path_for_callback):
        raise ValueError("Callback path contains disallowed traversal components")

    # Construct the preliminary callback URL.
    callback_url = urllib.parse.urljoin(root_url, path_for_callback)

    # Append the state parameter securely.
    query = urllib.parse.urlencode({"state": session_token})
    callback_url_with_state = f"{callback_url}?{query}"

    # Parse the URL to extract the domain for validation.
    parsed = urllib.parse.urlparse(callback_url_with_state)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed callback URL")

    # Validate that the domain is in the allowed set.
    domain = parsed.hostname
    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not authorized for OAuth callbacks")

    return callback_url_with_state