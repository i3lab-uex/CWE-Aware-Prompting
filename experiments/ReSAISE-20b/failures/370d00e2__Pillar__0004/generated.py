import urllib.parse

# Allowed domains for OAuth callback URLs.  Add your own domain(s) here.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.example.org"}

def generate_oauth_token_url(app_base_url: str, token_path: str, session_state: str) -> str:
    """
    Build a fully‑qualified OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The main URL of the application (e.g. "https://app.example.com").
    token_path : str
        The path to the OAuth callback endpoint (e.g. "/oauth/callback").
    session_state : str
        A state token used to mitigate CSRF attacks.

    Returns
    -------
    str
        The complete callback URL with a `state` query parameter.

    Raises
    ------
    ValueError
        If the domain of the constructed URL is not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Ensure the base URL ends with a slash for proper joining
    if not app_base_url.endswith("/"):
        app_base_url += "/"

    # Join base URL and token path safely
    full_path = urllib.parse.urljoin(app_base_url, token_path.lstrip("/"))

    # Parse the URL to inspect its components
    parsed = urllib.parse.urlparse(full_path)

    # Verify that the domain is allowed
    host = parsed.hostname
    if host not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Unauthorized callback domain: {host!r}")

    # Build the query string with an encoded state value
    query = urllib.parse.urlencode({"state": session_state})

    # Reconstruct the URL with the new query component
    oauth_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            query,
            parsed.fragment,
        )
    )

    return oauth_url