import urllib.parse

# Domains that are allowed for OAuth callback URLs.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed
}

def build_oauth_redirect_url(main_url: str, redirect_endpoint: str, session_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g. "https://app.example.com").
    redirect_endpoint : str
        The path to the OAuth callback handler (e.g. "/auth/callback").
    session_state : str
        A unique state value used to maintain integrity of the OAuth exchange.

    Returns
    -------
    str
        The fully assembled callback URL with state parameter appended.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in ``ALLOWED_CALLBACK_DOMAINS`` and
        does not match the domain of ``main_url``.
    """
    # Normalize input URLs
    base = main_url.rstrip("/")
    endpoint = redirect_endpoint.lstrip("/")

    # Build the full callback URL
    full_url = urllib.parse.urljoin(base + "/", endpoint)

    # Parse domains for validation
    parsed_main = urllib.parse.urlparse(main_url)
    parsed_full = urllib.parse.urlparse(full_url)

    main_domain = parsed_main.hostname.lower() if parsed_main.hostname else ""
    full_domain = parsed_full.hostname.lower() if parsed_full.hostname else ""

    # Enforce domain restrictions
    allowed = (
        full_domain in ALLOWED_CALLBACK_DOMAINS or
        full_domain == main_domain
    )
    if not allowed:
        raise ValueError(
            f"Disallowed callback domain: {full_domain}. "
            f"Allowed domains: {ALLOWED_CALLBACK_DOMAINS}"
        )

    # Append the state parameter safely
    query = urllib.parse.urlencode({"state": session_state})
    callback_url = f"{full_url}?{query}"

    return callback_url