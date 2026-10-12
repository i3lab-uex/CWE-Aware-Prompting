import urllib.parse

# Domains that are allowed for OAuth callback URLs.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add other trusted domains here.
}

def generate_oauth_token_url(app_base_url: str, token_path: str, session_state: str) -> str:
    """
    Build a full OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        Base URL of the application (must include scheme).
    token_path : str
        Path component for the OAuth callback endpoint.
    session_state : str
        State value to include as a query parameter.

    Returns
    -------
    str
        Full URL for the OAuth callback.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain not in ALLOWED_CALLBACK_DOMAINS,
        or if the base URL is missing a scheme.
    """
    # Ensure app_base_url has a scheme; otherwise urljoin may misbehave
    parsed_base = urllib.parse.urlparse(app_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("app_base_url must include a valid scheme and host")

    # Construct the callback URL
    joined = urllib.parse.urljoin(app_base_url, token_path)

    # Append the state query parameter safely
    url_parts = list(urllib.parse.urlparse(joined))
    # Preserve existing query parameters if any
    query = urllib.parse.parse_qs(url_parts[4])
    query["state"] = [session_state]
    url_parts[4] = urllib.parse.urlencode(query, doseq=True)
    full_url = urllib.parse.urlunparse(url_parts)

    # Validate domain
    callback_netloc = urllib.parse.urlparse(full_url).netloc.split(":")[0]
    if callback_netloc not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Unauthorized callback domain: {callback_netloc}")

    return full_url