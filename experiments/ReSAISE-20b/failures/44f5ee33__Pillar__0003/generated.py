import urllib.parse

# Domains that are permitted to receive the OAuth callback.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add other trusted domains here
}

def build_oauth_redirect_url(main_url: str, redirect_path: str, nonce: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g., "https://app.example.com").
    redirect_path : str
        The relative path where the OAuth provider should redirect to
        (e.g., "/auth/callback").
    nonce : str
        A cryptographically random string used as the state parameter to
        prevent CSRF attacks.

    Returns
    -------
    str
        The fully qualified callback URL, including the state query
        parameter.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in
        ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Ensure the main_url is absolute and parse it
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError(f"Invalid main_url: {main_url!r}")

    # Build the callback URL by joining the base with the redirect path
    joined_url = urllib.parse.urljoin(main_url, redirect_path)

    # Parse the resulting URL to inspect its components
    parsed_callback = urllib.parse.urlparse(joined_url)

    # Extract the hostname and validate it against allowed domains
    host = parsed_callback.hostname
    if not host or host.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Unauthorized callback domain: {host!r}")

    # Append the state (nonce) as a query parameter
    query_params = urllib.parse.parse_qs(parsed_callback.query)
    # Preserve existing parameters if any
    query_params["state"] = [nonce]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the full URL with the new query string
    final_url = urllib.parse.urlunparse((
        parsed_callback.scheme,
        parsed_callback.netloc,
        parsed_callback.path,
        parsed_callback.params,
        new_query,
        parsed_callback.fragment
    ))

    return final_url