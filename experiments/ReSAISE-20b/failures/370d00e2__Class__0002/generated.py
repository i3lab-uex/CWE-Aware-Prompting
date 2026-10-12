import urllib.parse

# Set of domains that are allowed for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add more trusted domains here
}


def generate_oauth_token_url(app_base_url: str, token_path: str, session_state: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The main base URL of the application (e.g. "https://app.example.com").
    token_path : str
        The path to the OAuth callback endpoint (e.g. "/oauth/callback").
    session_state : str
        A cryptographically random string used to verify the OAuth transaction.

    Returns
    -------
    str
        The fully qualified callback URL with query parameters appended.

    Raises
    ------
    ValueError
        If the resulting callback URL points to an unauthorized domain or uses an
        insecure scheme.
    """
    # Normalize and join the base URL with the token path.
    joined_url = urllib.parse.urljoin(app_base_url.rstrip("/") + "/", token_path.lstrip("/"))

    # Parse the URL to inspect components.
    parsed = urllib.parse.urlparse(joined_url)

    # Ensure scheme is HTTPS; reject HTTP or missing scheme.
    if parsed.scheme.lower() != "https":
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}'. Only HTTPS is allowed.")

    # Ensure the domain (netloc) is in the whitelist.
    domain = parsed.hostname
    if not domain or domain.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not authorized for OAuth callbacks.")

    # Append the state parameter as a query string.
    query = urllib.parse.urlencode({"state": session_state})
    final_url = parsed._replace(query=query).geturl()

    return final_url