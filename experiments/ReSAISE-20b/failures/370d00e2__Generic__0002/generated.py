import urllib.parse

# Example allowed domains; in real usage this should be configured securely.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.myapp.io"}

def generate_oauth_token_url(app_base_url: str, token_path: str, session_state: str) -> str:
    """
    Build a full OAuth callback URL from the application base, token path and state.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g. "https://myapp.com").
    token_path : str
        The path that will handle the OAuth callback (e.g. "/auth/callback").
    session_state : str
        A CSRF‑protecting state value to include in the query string.

    Returns
    -------
    str
        The fully-qualified OAuth callback URL.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in
        :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Normalize base URL (ensure it ends with a slash for urljoin to work correctly)
    if not app_base_url.endswith("/"):
        base = f"{app_base_url}/"
    else:
        base = app_base_url

    # Join the base and path
    full_path = urllib.parse.urljoin(base, token_path)

    # Parse the resulting URL to extract its components
    parsed = urllib.parse.urlparse(full_path)

    # Validate the domain against allowed list (case‑insensitive)
    hostname = parsed.hostname
    if not hostname or hostname.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Unauthorized callback domain: {hostname!r}")

    # Append the state parameter
    query_params = urllib.parse.parse_qs(parsed.query)
    query_params["state"] = [session_state]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the URL with updated query
    new_parsed = parsed._replace(query=new_query)
    return urllib.parse.urlunparse(new_parsed)


# Example usage
if __name__ == "__main__":
    try:
        url = generate_oauth_token_url(
            app_base_url="https://example.com",
            token_path="/oauth/callback",
            session_state="abc123XYZ"
        )
        print("OAuth callback URL:", url)
    except ValueError as e:
        print("Error:", e)