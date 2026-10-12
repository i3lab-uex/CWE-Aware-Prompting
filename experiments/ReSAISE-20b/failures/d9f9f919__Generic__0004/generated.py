import urllib.parse

# List of external domains that are explicitly allowed for redirects.
ALLOWED_DOMAINS = {
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed
}

def build_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Build a safe redirect URL for post‑login navigation.

    Parameters
    ----------
    app_base_url : str
        The base authentication URL of the application (e.g. "https://myapp.com/login").
    redirect_param : str
        The URL path or full URL supplied by the user to navigate to after login.

    Returns
    -------
    str
        The fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe (i.e. outside the base domain and not in ALLOWED_DOMAINS).
    """
    # Parse the base URL once.
    base_parsed = urllib.parse.urlparse(app_base_url)

    # Resolve the redirect_param relative to the base URL.
    joined = urllib.parse.urljoin(app_base_url, redirect_param)

    # Parse the resulting URL.
    result_parsed = urllib.parse.urlparse(joined)

    # Ensure scheme is http or https.
    if result_parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {result_parsed.scheme}")

    # If the redirect is relative (no netloc) or points to the same host, it's safe.
    if not result_parsed.netloc or result_parsed.netloc == base_parsed.netloc:
        return joined

    # If the redirect points to an allowed external domain, allow it.
    host = result_parsed.hostname
    if host in ALLOWED_DOMAINS:
        return joined

    # Otherwise, reject the redirect.
    raise ValueError(
        f"Redirect URL '{joined}' is not allowed. "
        f"Target domain '{host}' is outside the permitted domains."
    )