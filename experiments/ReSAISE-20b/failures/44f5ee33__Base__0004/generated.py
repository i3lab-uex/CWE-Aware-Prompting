import urllib.parse

# Domains that are allowed to receive OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
}

def build_oauth_redirect_url(main_url: str, redirect_path: str, nonce: str) -> str:
    """
    Build a safe OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g., "https://app.example.com").
    redirect_path : str
        The path where the OAuth provider should redirect to (e.g., "/oauth/callback").
    nonce : str
        A unique state value that will be passed to the OAuth provider.

    Returns
    -------
    str
        A fully qualified callback URL that includes the state parameter.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in
        ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Ensure the redirect path is properly joined to the main URL
    base = urllib.parse.urljoin(main_url.rstrip("/") + "/", redirect_path.lstrip("/"))

    # Append the nonce as a query parameter named `state`
    parsed = urllib.parse.urlparse(base)
    qs = dict(urllib.parse.parse_qsl(parsed.query))
    qs["state"] = nonce
    new_query = urllib.parse.urlencode(qs)
    safe_url = parsed._replace(query=new_query).geturl()

    # Validate that the domain is authorized
    host = urllib.parse.urlparse(safe_url).hostname or ""
    # Normalize to lower case for comparison
    host = host.lower()
    if host not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Unauthorized callback domain: {host}")

    return safe_url