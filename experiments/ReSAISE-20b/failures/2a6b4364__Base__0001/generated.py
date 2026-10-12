import re
from urllib.parse import urlparse, urljoin

# List of domains considered safe for redirection
ALLOWED_DOMAINS = [
    "example.com",
    "sub.example.com",
    # Add other trusted domains here
]

# Regex to detect if a URL is absolute (contains scheme)
_ABSOLUTE_URL_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://")

def _is_absolute(url: str) -> bool:
    """Return True if the URL contains a scheme."""
    return _ABSOLUTE_URL_RE.match(url) is not None

def create_redirect_url(base_url: str, next_param: str) -> str:
    """
    Construct a safe redirect URL.

    Parameters
    ----------
    base_url : str
        The base URL of the application (e.g., "https://myapp.com").
    next_param : str
        The user-provided 'next' parameter. It may be a relative path or an absolute URL.

    Returns
    -------
    str
        A fully resolved redirect URL that is either relative to ``base_url`` or points to an allowed domain.

    Raises
    ------
    ValueError
        If ``next_param`` resolves to a URL that is not within the same domain as ``base_url``
        and does not belong to one of the :data:`ALLOWED_DOMAINS`.
    """
    # Sanitize base_url
    parsed_base = urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base_url: {base_url!r}")

    # Resolve the next_param against the base URL
    resolved = urljoin(base_url, next_param)

    parsed_resolved = urlparse(resolved)

    # If the resolved URL is relative (no scheme), we are safe
    if not parsed_resolved.scheme:
        return resolved

    # Check that the scheme is HTTP/HTTPS
    if parsed_resolved.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed_resolved.scheme!r}")

    # If the host is the same as the base URL's host, we allow it
    if parsed_resolved.netloc == parsed_base.netloc:
        return resolved

    # Otherwise, ensure the host is in ALLOWED_DOMAINS
    host = parsed_resolved.hostname or ""
    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Redirect to untrusted domain: {host!r}")

    # All checks passed – return the fully resolved URL
    return resolved

# Example usage:
if __name__ == "__main__":
    base = "https://myapp.com"
    for nxt in [
        "/dashboard",
        "../login",
        "https://myapp.com/profile",
        "http://example.com/welcome",
        "http://malicious.com/phish"
    ]:
        try:
            print(f"next={nxt!r} -> {create_redirect_url(base, nxt)}")
        except ValueError as e:
            print(f"next={nxt!r} -> Error: {e}")