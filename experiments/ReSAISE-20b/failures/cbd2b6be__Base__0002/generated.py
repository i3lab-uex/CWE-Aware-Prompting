import urllib.parse

# Example set of allowed domains – replace with your actual list.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add more domains as needed
}


def build_oauth_redirect_url(main_url: str, redirect_path: str, token_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g. "https://app.example.com").
    redirect_path : str
        The path component for the OAuth callback (e.g. "/oauth/callback").
    token_state : str
        A unique state value to mitigate CSRF attacks.

    Returns
    -------
    str
        The fully-qualified redirect URL with the state query parameter appended.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Normalise the base URL and path
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError(f"Invalid main_url: {main_url!r}")

    # Ensure redirect_path is relative (no scheme/netloc)
    parsed_redirect = urllib.parse.urlparse(redirect_path)
    if parsed_redirect.scheme or parsed_redirect.netloc:
        raise ValueError("redirect_path must be a relative path, not an absolute URL")

    # Build the full path by joining main_url with redirect_path
    joined = urllib.parse.urljoin(main_url.rstrip('/') + '/', redirect_path.lstrip('/'))

    # Append the state parameter
    url_parts = list(urllib.parse.urlparse(joined))
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    query['state'] = token_state
    url_parts[4] = urllib.parse.urlencode(query)
    final_url = urllib.parse.urlunparse(url_parts)

    # Verify the domain is allowed
    domain = urllib.parse.urlparse(final_url).hostname
    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Disallowed callback domain: {domain!r}")

    return final_url