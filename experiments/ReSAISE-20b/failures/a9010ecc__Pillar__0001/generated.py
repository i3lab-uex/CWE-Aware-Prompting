import urllib.parse

# List of external domains considered safe for redirection.
ALLOWED_DOMAINS = {"example.com", "trusted.org"}

def generate_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Build a safe redirect URL after login.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g., "https://myapp.com/").
    redirect_param : str
        The URL path or full URL the user wishes to navigate to after login.

    Returns
    -------
    str
        A fully resolved redirect URL that is either within the same host as
        `app_base_url` or one of the domains listed in ``ALLOWED_DOMAINS``.

    Raises
    ------
    ValueError
        If the constructed URL points outside of the base domain or to a domain
        not present in ``ALLOWED_DOMAINS``.
    """
    # Resolve the redirect URL relative to the base application URL.
    full_url = urllib.parse.urljoin(app_base_url, redirect_param)

    # Parse the components of both URLs.
    base_parsed = urllib.parse.urlparse(app_base_url)
    redirect_parsed = urllib.parse.urlparse(full_url)

    # Normalize netlocs by removing default ports.
    def normalize_netloc(netloc: str) -> str:
        host, _, port = netloc.partition(":")
        return f"{host.lower()}:{port}" if port else host.lower()

    base_netloc = normalize_netloc(base_parsed.netloc)
    redirect_netloc = normalize_netloc(redirect_parsed.netloc)

    # If the redirect points to the same host, accept it.
    if base_netloc == redirect_netloc:
        return full_url

    # Otherwise, ensure the host is in ALLOWED_DOMAINS.
    redirect_host = redirect_parsed.hostname.lower() if redirect_parsed.hostname else ""
    if redirect_host in ALLOWED_DOMAINS:
        return full_url

    # If we reach here, the redirect is unsafe.
    raise ValueError(
        f"Unsafe redirect target: {full_url} "
        f"(base host: {base_netloc}, allowed domains: {ALLOWED_DOMAINS})"
    )