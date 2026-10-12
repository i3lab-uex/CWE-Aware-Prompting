import urllib.parse

# Domains allowed for OAuth callback URLs (example values)
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
}

def build_oauth_redirect_url(main_url: str, redirect_path: str, nonce: str) -> str:
    """
    Construct a safe OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g. "https://app.example.com").
    redirect_path : str
        The path that handles the OAuth callback (e.g. "/auth/callback").
    nonce : str
        A state value used to protect against CSRF.

    Returns
    -------
    str
        The fully qualified redirect URL with the state parameter appended.

    Raises
    ------
    ValueError
        If the resulting URL resolves to an unauthorized domain or if
        `redirect_path` contains a scheme/netloc (potential open redirect).
    """
    # Ensure the redirect path is relative and does not contain a scheme/netloc
    parsed_path = urllib.parse.urlparse(redirect_path)
    if parsed_path.scheme or parsed_path.netloc:
        raise ValueError("Redirect path must be relative and not contain a scheme or netloc")

    # Join the main URL with the redirect path
    joined_url = urllib.parse.urljoin(main_url, redirect_path)

    # Parse the combined URL to inspect its components
    parsed = urllib.parse.urlparse(joined_url)

    # Validate that the host is in the allowed set
    hostname = parsed.hostname
    if not hostname or hostname.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Unauthorized callback domain: {hostname}")

    # Append the nonce as a 'state' query parameter
    query_params = urllib.parse.parse_qs(parsed.query)
    # Overwrite any existing 'state' parameter to prevent tampering
    query_params["state"] = [nonce]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the final URL
    safe_url = urllib.parse.urlunparse(
        parsed._replace(query=new_query)
    )

    return safe_url