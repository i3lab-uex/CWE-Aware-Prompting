import urllib.parse

# List of external domains that are considered safe for redirection.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedsite.org",
    "myapp.example.com",
]

def create_forward_link(app_home_url: str, forward_param: str) -> str:
    """
    Construct a safe redirect URL.

    Parameters
    ----------
    app_home_url : str
        Base URL of the application (e.g. "https://myapp.example.com").
    forward_param : str
        Desired redirect path or absolute URL provided by the user.

    Returns
    -------
    str
        The fully-qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the base domain or an allowed external domain.
    """
    # Ensure app_home_url has a scheme and netloc
    base_parsed = urllib.parse.urlparse(app_home_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("app_home_url must be a valid absolute URL")

    # Resolve the forward_param against the base URL
    target_url = urllib.parse.urljoin(app_home_url, forward_param)

    # Parse the resulting URL
    parsed = urllib.parse.urlparse(target_url)

    # If netloc is empty, the URL is relative and safe (already resolved above)
    if not parsed.netloc:
        return target_url

    # For absolute URLs, check that the domain is allowed
    # Extract hostname (netloc may contain port)
    host = parsed.hostname or ""
    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Redirection to external domain '{host}' is not allowed")

    # Ensure the scheme is HTTP/HTTPS
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only HTTP and HTTPS schemes are allowed for redirects")

    return target_url