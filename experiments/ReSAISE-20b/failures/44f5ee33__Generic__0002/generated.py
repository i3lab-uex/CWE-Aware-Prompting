import urllib.parse

# Example set of allowed callback domains.
# In a real application this should be populated with the actual trusted domains.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "sub.example.org",
}

def build_oauth_redirect_url(main_url: str, redirect_path: str, nonce: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g., "https://myapp.com").
    redirect_path : str
        The path that should handle the OAuth callback (e.g., "/oauth/callback").
    nonce : str
        A random string used as the state parameter to mitigate CSRF attacks.

    Returns
    -------
    str
        The fully qualified callback URL including the state query parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL resolves to a domain not in
        ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Ensure we have a proper base URL
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError(f"Invalid main_url: {main_url!r}")

    # Construct the absolute callback URL
    callback = urllib.parse.urljoin(main_url, redirect_path)

    # Append the state parameter (nonce) as a query string
    parsed_callback = urllib.parse.urlparse(callback)
    query_params = dict(urllib.parse.parse_qsl(parsed_callback.query))
    query_params["state"] = nonce
    new_query = urllib.parse.urlencode(query_params)

    callback_with_state = parsed_callback._replace(query=new_query).geturl()

    # Validate the domain of the callback URL
    callback_domain = urllib.parse.urlparse(callback_with_state).hostname
    if callback_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Unauthorized callback domain: {callback_domain!r}. "
            f"Allowed domains are: {', '.join(sorted(ALLOWED_CALLBACK_DOMAINS))}"
        )

    return callback_with_state