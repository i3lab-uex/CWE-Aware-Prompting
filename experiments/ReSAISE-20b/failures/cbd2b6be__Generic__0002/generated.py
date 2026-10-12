import urllib.parse

# Example list of allowed callback domains.  In a real application this would be
# defined in your configuration or environment variables.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
}

def build_oauth_redirect_url(main_url: str, redirect_path: str, token_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g. "https://myapp.com").
    redirect_path : str
        The path to the OAuth callback endpoint (e.g. "/oauth/callback").
    token_state : str
        A unique value used to verify the integrity of the OAuth flow.

    Returns
    -------
    str
        The fully qualified redirect URL including a `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Normalise the base URL and path
    base = main_url.rstrip("/")
    path = redirect_path.lstrip("/")

    # Build the absolute URL
    url = urllib.parse.urljoin(base + "/", path)

    # Append the state query parameter
    parsed = urllib.parse.urlparse(url)
    query_params = dict(urllib.parse.parse_qsl(parsed.query))
    query_params["state"] = token_state
    new_query = urllib.parse.urlencode(query_params)
    url_with_state = parsed._replace(query=new_query).geturl()

    # Validate the domain
    netloc = urllib.parse.urlparse(url_with_state).netloc.lower()
    # Remove port if present
    domain = netloc.split(":")[0]
    if not any(domain == allowed or domain.endswith("." + allowed) for allowed in ALLOWED_CALLBACK_DOMAINS):
        raise ValueError(f"Callback domain '{domain}' is not allowed.")

    return url_with_state