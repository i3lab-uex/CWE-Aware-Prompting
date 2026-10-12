import urllib.parse

# Pre‑approved external domains that may be used for redirection.
ALLOWED_DOMAINS = {"example.com", "trusted.org"}

def build_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Build a safe redirect URL after login.

    Parameters
    ----------
    app_base_url : str
        Base authentication URL of the application (e.g. "https://app.example.com/login").
    redirect_param : str
        URL path or full URL supplied by the user to navigate after login.

    Returns
    -------
    str
        A fully resolved redirect URL that is safe for use.

    Raises
    ------
    ValueError
        If the resolved URL points outside the base domain and is not in
        ALLOWED_DOMAINS.
    """
    # Parse the base URL once.
    base_parsed = urllib.parse.urlparse(app_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("Invalid app_base_url: missing scheme or netloc")

    # Resolve the redirect_param against the base URL.
    resolved_url = urllib.parse.urljoin(app_base_url, redirect_param)

    # Parse the resolved URL for validation.
    parsed = urllib.parse.urlparse(resolved_url)

    # If the redirect is relative (no netloc), it stays within the base domain.
    if not parsed.netloc:
        return resolved_url

    # If the netloc matches the base domain, it's safe.
    if parsed.netloc.lower() == base_parsed.netloc.lower():
        return resolved_url

    # If the netloc is in ALLOWED_DOMAINS, allow it.
    host = parsed.hostname or ""
    if host.lower() in ALLOWED_DOMAINS:
        return resolved_url

    # Otherwise, the URL is unsafe.
    raise ValueError(f"Unsafe redirect target: {resolved_url}")