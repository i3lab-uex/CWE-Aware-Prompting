import urllib.parse

# Example list of allowed domains; replace with your actual list.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    "oauth.partner.net"
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
        A unique value to protect against CSRF attacks.

    Returns
    -------
    str
        The fully-qualified callback URL with a state query parameter.

    Raises
    ------
    ValueError
        If the domain of the constructed URL is not in ALLOWED_CALLBACK_DOMAINS.
    """
    # Build the base callback URL by joining main_url and redirect_path
    # urllib.parse.urljoin handles leading/trailing slashes appropriately.
    base_callback_url = urllib.parse.urljoin(main_url.rstrip('/') + '/', redirect_path.lstrip('/'))

    # Parse the URL to inspect its domain
    parsed = urllib.parse.urlparse(base_callback_url)
    domain = parsed.netloc.lower()

    # If the URL contains a port, strip it for domain comparison
    if ':' in domain:
        domain = domain.split(':')[0]

    # Ensure the callback domain is allowed
    if domain not in {d.lower() for d in ALLOWED_CALLBACK_DOMAINS}:
        raise ValueError(f"Callback domain '{domain}' is not allowed.")

    # Append the state parameter securely
    query = urllib.parse.parse_qs(parsed.query)
    query['state'] = [token_state]  # parse_qs returns lists

    # Reconstruct the query string, preserving existing parameters
    new_query = urllib.parse.urlencode(query, doseq=True)

    # Build the final URL
    final_url = urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))

    return final_url