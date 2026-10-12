import urllib.parse

# Domains that are allowed to be used as the callback host.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.example.org"}

def build_oauth_redirect_url(main_url: str, redirect_path: str, nonce: str) -> str:
    """
    Build a full OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application, e.g. "https://myapp.com".
    redirect_path : str
        The path to use for the OAuth callback, e.g. "/auth/callback".
        If an absolute URL is supplied it will be validated against
        :data:`ALLOWED_CALLBACK_DOMAINS` and rejected if the domain is not allowed.
    nonce : str
        A cryptographically random string that will be passed as the `state`
        query parameter to protect against CSRF.

    Returns
    -------
    str
        The fully-qualified OAuth callback URL including the state parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL resolves to a domain that is not in
        :data:`ALLOWED_CALLBACK_DOMAINS` or if the supplied ``redirect_path`` is
        an absolute URL pointing to a disallowed domain.
    """
    # Normalize the main URL and redirect path
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError(f"Invalid main URL: {main_url!r}")

    # If redirect_path is an absolute URL, validate it directly
    parsed_redirect = urllib.parse.urlparse(redirect_path)
    if parsed_redirect.scheme and parsed_redirect.netloc:
        domain = parsed_redirect.hostname
        if domain not in ALLOWED_CALLBACK_DOMAINS:
            raise ValueError(f"Disallowed callback domain: {domain!r}")
        # Append state parameter
        query = urllib.parse.parse_qs(parsed_redirect.query)
        query["state"] = [nonce]
        new_query = urllib.parse.urlencode(query, doseq=True)
        return parsed_redirect._replace(query=new_query).geturl()

    # Otherwise, treat redirect_path as a relative path
    joined = urllib.parse.urljoin(main_url.rstrip("/") + "/", redirect_path.lstrip("/"))
    parsed_joined = urllib.parse.urlparse(joined)

    # Ensure the domain is allowed
    if parsed_joined.hostname not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Disallowed callback domain: {parsed_joined.hostname!r}")

    # Append the state parameter
    query = urllib.parse.parse_qs(parsed_joined.query)
    query["state"] = [nonce]
    new_query = urllib.parse.urlencode(query, doseq=True)
    return parsed_joined._replace(query=new_query).geturl()