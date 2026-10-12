import urllib.parse

# Define the domains that are considered safe for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    "localhost",
}

def build_oauth_redirect_url(main_url: str, redirect_path: str, token_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The application's base URL (e.g., "https://app.example.com").
    redirect_path : str
        The path component for the OAuth callback (e.g., "/auth/callback").
    token_state : str
        A unique value used to verify the integrity of the OAuth flow.

    Returns
    -------
    str
        The fully qualified callback URL with the state query parameter appended.

    Raises
    ------
    ValueError
        If the resolved callback URL's domain is not in ALLOWED_CALLBACK_DOMAINS.
    """
    # Ensure the redirect path is a relative URL component.
    if urllib.parse.urlparse(redirect_path).scheme:
        raise ValueError("Redirect path must be a relative path, not an absolute URL.")

    # Build the full callback URL.
    base = urllib.parse.urljoin(main_url.rstrip('/') + '/', redirect_path.lstrip('/'))
    parsed = urllib.parse.urlparse(base)

    # Validate the domain against the allowed list.
    hostname = parsed.hostname or ""
    if not hostname:
        raise ValueError("Callback URL must contain a valid domain.")

    # Strip port if present and compare case-insensitively.
    hostname = hostname.lower()
    if hostname not in {d.lower() for d in ALLOWED_CALLBACK_DOMAINS}:
        raise ValueError(f"Domain '{hostname}' is not allowed for OAuth callbacks.")

    # Append the state query parameter securely.
    query = urllib.parse.parse_qs(parsed.query)
    query["state"] = [token_state]
    new_query = urllib.parse.urlencode(query, doseq=True)

    # Reconstruct the final URL.
    final_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment,
        )
    )

    return final_url