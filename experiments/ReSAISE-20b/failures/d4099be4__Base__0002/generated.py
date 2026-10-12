import urllib.parse

# Domains that are considered safe for OAuth callback redirects.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    "login.myapp.io",
}

def generate_oauth_callback_link(
    app_base_url: str,
    callback_endpoint: str,
    verification_state: str
) -> str:
    """
    Build a fully‑qualified OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The main base URL of the application (e.g. "https://app.example.com").
    callback_endpoint : str
        The path to the OAuth callback endpoint (e.g. "/oauth/callback").
    verification_state : str
        A unique value used to verify the integrity of the OAuth flow.

    Returns
    -------
    str
        The complete callback URL with state query parameter appended.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Normalise the base URL (ensure it ends with a slash)
    if not app_base_url.endswith("/"):
        app_base_url += "/"

    # Join base and endpoint safely
    callback_url = urllib.parse.urljoin(app_base_url, callback_endpoint)

    # Parse the URL to extract components
    parsed = urllib.parse.urlparse(callback_url)

    # Validate domain against allowed list
    host = parsed.hostname or ""
    if host.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Disallowed callback domain: {host}")

    # Append the state query parameter
    query = urllib.parse.urlencode({"state": verification_state})
    final_url = urllib.parse.urlunparse(
        parsed._replace(query=query)
    )

    return final_url