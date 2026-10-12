import urllib.parse

# Example set of allowed callback domains; replace with actual values.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.myapp.com"}


def build_oauth_redirect_url(main_url: str, redirect_path: str, nonce: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g., "https://myapp.com").
    redirect_path : str
        The path to the OAuth callback endpoint (e.g., "/oauth/callback").
    nonce : str
        A state parameter to mitigate CSRF attacks.

    Returns
    -------
    str
        The fully qualified callback URL, including the nonce as a query parameter.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in ALLOWED_CALLBACK_DOMAINS.
    """
    # Ensure redirect_path starts with a slash
    if not redirect_path.startswith("/"):
        redirect_path = "/" + redirect_path

    # Build the base URL
    joined_url = urllib.parse.urljoin(main_url.rstrip("/") + "/", redirect_path.lstrip("/"))

    # Append the nonce as a query parameter
    parsed = urllib.parse.urlparse(joined_url)
    query_params = dict(urllib.parse.parse_qsl(parsed.query))
    query_params["state"] = nonce
    new_query = urllib.parse.urlencode(query_params)
    rebuilt_url = parsed._replace(query=new_query).geturl()

    # Validate the domain
    netloc = urllib.parse.urlparse(rebuilt_url).netloc.lower()
    # Remove port if present
    domain = netloc.split(":")[0]
    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Unauthorized callback domain: {domain}")

    return rebuilt_url