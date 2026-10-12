import urllib.parse

# Predefined set of domains allowed for OAuth callbacks
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.example.org"}

def build_oauth_redirect_url(main_url: str, redirect_endpoint: str, session_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The root URL of the application (e.g., 'https://app.example.com').
    redirect_endpoint : str
        The endpoint path for the OAuth callback (e.g., '/oauth/callback').
    session_state : str
        A unique identifier used to maintain the integrity of the OAuth exchange.

    Returns
    -------
    str
        The fully assembled, validated callback URL.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in ALLOWED_CALLBACK_DOMAINS and does not match
        the domain of `main_url`. This protects against open‑redirect attacks (CWE‑601).
    """
    # Ensure the redirect endpoint starts with a slash
    if not redirect_endpoint.startswith("/"):
        redirect_endpoint = "/" + redirect_endpoint

    # Construct the base callback URL
    callback_url = urllib.parse.urljoin(main_url, redirect_endpoint)

    # Parse the resulting URL to inspect its components
    parsed = urllib.parse.urlparse(callback_url)

    # Validate the scheme (must be https for security)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate the domain
    host = parsed.hostname or ""
    if host not in ALLOWED_CALLBACK_DOMAINS:
        # Fallback: allow the domain to match the main_url's host
        main_host = urllib.parse.urlparse(main_url).hostname or ""
        if host != main_host:
            raise ValueError(
                f"Callback domain '{host}' is not allowed. "
                f"Allowed domains: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
            )

    # Append the state parameter
    query = urllib.parse.urlencode({"state": session_state})
    final_url_parts = parsed._replace(query=query)
    return urllib.parse.urlunparse(final_url_parts)

# Example usage:
if __name__ == "__main__":
    try:
        url = build_oauth_redirect_url(
            main_url="https://app.example.com",
            redirect_endpoint="/oauth/callback",
            session_state="xyz123"
        )
        print(url)
    except ValueError as e:
        print(f"Invalid callback URL: {e}")