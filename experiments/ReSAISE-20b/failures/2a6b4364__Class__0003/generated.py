import urllib.parse

# Domains that are explicitly allowed for redirection (e.g. trusted partners)
ALLOWED_DOMAINS = ["trustedpartner.com", "anotherdomain.org"]

def create_redirect_url(base_url: str, next_param: str) -> str:
    """
    Build a safe redirect URL.

    Parameters
    ----------
    base_url : str
        The base URL of the application (e.g. "https://example.com").
    next_param : str
        The user-provided 'next' parameter that may be a relative or absolute URL.

    Returns
    -------
    str
        A fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the same domain as ``base_url`` or an allowed external
        domain, or if it contains an unsafe scheme.
    """
    # Parse the base URL to extract its components
    base_parsed = urllib.parse.urlparse(base_url)

    # Resolve the next_param against the base URL
    resolved = urllib.parse.urljoin(base_url, next_param)

    # Parse the resulting URL
    parsed = urllib.parse.urlparse(resolved)

    # Ensure scheme is http or https (prevent file://, data:, etc.)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Disallowed scheme: {parsed.scheme}")

    # Compare netloc (domain + port)
    base_netloc = base_parsed.netloc.lower()
    target_netloc = parsed.netloc.lower()

    # If the target domain is the same as base, accept
    if target_netloc == base_netloc:
        return resolved

    # If the target domain is in ALLOWED_DOMAINS, accept
    host = parsed.hostname.lower() if parsed.hostname else ""
    if host in [d.lower() for d in ALLOWED_DOMAINS]:
        return resolved

    # Otherwise, reject
    raise ValueError(f"Redirect target '{resolved}' is not allowed")