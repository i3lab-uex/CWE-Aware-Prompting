import urllib.parse

# List of external domains that are considered safe for redirection.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    "secure.example.net"
]

def construct_redirect_link(domain_base_url: str, next_redirect_param: str) -> str:
    """
    Construct a safe redirect URL.

    Parameters
    ----------
    domain_base_url : str
        Base URL of the application (e.g., "https://myapp.com").
    next_redirect_param : str
        User-provided redirect target. May be a relative path or an absolute URL.

    Returns
    -------
    str
        The fully-qualified redirect URL that is guaranteed to be within the
        application's domain or an allowed external domain.

    Raises
    ------
    ValueError
        If the resulting URL is not within the base domain or an allowed
        external domain.
    """
    # Parse the base URL once for reuse
    parsed_base = urllib.parse.urlparse(domain_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base URL")

    # Resolve the next_redirect_param relative to the base
    joined_url = urllib.parse.urljoin(domain_base_url, next_redirect_param)

    parsed_joined = urllib.parse.urlparse(joined_url)

    # 1. If the scheme is empty or http/https and netloc matches base -> ok
    if parsed_joined.scheme in ("", "http", "https"):
        # If netloc is empty, it's a relative path within the base domain
        if not parsed_joined.netloc:
            return urllib.parse.urlunparse(parsed_joined)

        # If netloc matches base domain (case-insensitive)
        if parsed_joined.netloc.lower() == parsed_base.netloc.lower():
            return urllib.parse.urlunparse(parsed_joined)

        # If netloc is in allowed domains list
        host = parsed_joined.netloc.split(":")[0].lower()
        if host in ALLOWED_DOMAINS:
            return urllib.parse.urlunparse(parsed_joined)

    # If we reach here, the URL is not allowed
    raise ValueError(f"Disallowed redirect target: {joined_url}")