import urllib.parse

# Domains considered safe for external redirection.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
]

def create_redirect_url(base_url: str, next_param: str) -> str:
    """
    Construct a safe redirect URL by combining the application's base URL with
    a user-provided `next` parameter.

    Parameters
    ----------
    base_url : str
        The base URL of the application (e.g. "https://app.example.com/").
    next_param : str
        The user supplied redirect target (may be a relative path or an absolute URL).

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not on the same domain as `base_url` or one of
        the explicitly allowed external domains.
    """
    # Normalise base URL to ensure it ends with a slash
    if not base_url.endswith("/"):
        base_url = f"{base_url}/"

    # Resolve the next_param against the base URL
    joined = urllib.parse.urljoin(base_url, next_param)

    # Parse both URLs for comparison
    base_parsed = urllib.parse.urlparse(base_url)
    joined_parsed = urllib.parse.urlparse(joined)

    # Helper to normalize netloc (strip default ports)
    def _normalize_netloc(netloc: str) -> str:
        host, sep, port = netloc.partition(":")
        if (port == "80" and base_parsed.scheme == "http") or \
           (port == "443" and base_parsed.scheme == "https"):
            return host.lower()
        return netloc.lower()

    base_domain = _normalize_netloc(base_parsed.netloc)
    target_domain = _normalize_netloc(joined_parsed.netloc)

    # Allow relative URLs (empty netloc) or same-domain absolute URLs
    if target_domain and target_domain != base_domain:
        # If the target domain is not the same as the base, it must be in ALLOWED_DOMAINS
        if target_domain not in (d.lower() for d in ALLOWED_DOMAINS):
            raise ValueError(f"Redirect target '{joined}' is not allowed.")

    # Ensure the scheme matches (prevent http->https mismatch, etc.)
    if joined_parsed.scheme and joined_parsed.scheme != base_parsed.scheme:
        raise ValueError(f"Redirect target '{joined}' uses a different scheme.")

    return joined