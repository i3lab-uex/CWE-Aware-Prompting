import urllib.parse

# Domains that are considered safe for redirection.  These should be set to
# the domains your application truly owns or trusts.
ALLOWED_DOMAINS = {"example.com", "www.example.com"}

def create_redirect_url(base_url: str, next_param: str) -> str:
    """
    Build a safe redirect URL.

    Parameters
    ----------
    base_url : str
        The application's base URL (e.g., "https://www.example.com/").
    next_param : str
        The user supplied redirect target.  It may be a relative path,
        an absolute URL, or a fragment.

    Returns
    -------
    str
        A fully resolved redirect URL that is guaranteed to point to either
        the same host as `base_url` or one of the `ALLOWED_DOMAINS`.

    Raises
    ------
    ValueError
        If the resolved URL points to a domain that is not allowed.
    """
    if not base_url:
        raise ValueError("base_url must be a non-empty string")

    # Resolve the next_param against the base URL.
    # This handles relative paths and fragments correctly.
    resolved = urllib.parse.urljoin(base_url, next_param or "")

    parsed = urllib.parse.urlparse(resolved)
    # If the resulting URL is relative (no scheme/host), treat it as local.
    if not parsed.scheme and not parsed.netloc:
        return resolved

    # Normalize the domain for comparison (case‑insensitive, strip port)
    host = parsed.hostname or ""
    # Strip the default port if present
    if parsed.port:
        host = f"{host}:{parsed.port}"

    # Check that the domain is either the same as base_url or in ALLOWED_DOMAINS
    base_host = urllib.parse.urlparse(base_url).hostname
    if host.lower() == (base_host or "").lower():
        return resolved

    if host.lower() in {d.lower() for d in ALLOWED_DOMAINS}:
        return resolved

    # If we reach here, the target is not trusted.
    raise ValueError(f"Redirect URL {resolved} points to untrusted domain '{host}'")