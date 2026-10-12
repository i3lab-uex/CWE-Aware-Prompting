import re
from urllib.parse import urlparse, urlunparse

# List of domains that are allowed for redirection
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "safe-redirect.net",
}

# Regular expression to validate a domain (basic RFC 1035 compliance)
DOMAIN_RE = re.compile(r"^(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$")

def _is_approved_domain(domain: str) -> bool:
    """
    Return True if the domain is in APPROVED_DOMAINS.
    The comparison is case‑insensitive and ignores trailing dots.
    """
    domain = domain.lower().rstrip(".")
    return domain in APPROVED_DOMAINS

def process_url_redirect(input_url: str) -> str:
    """
    Validate that *input_url* points to an approved domain and return a safe URL.

    Parameters
    ----------
    input_url : str
        The URL supplied by the user.

    Returns
    -------
    str
        A validated and safe-to-use URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        or its domain is not in ``APPROVED_DOMAINS``.
    """
    if not isinstance(input_url, str):
        raise ValueError("URL must be a string")

    # Parse the URL; urlparse accepts many schemes but we restrict to http/https
    parsed = urlparse(input_url)

    # Reject URLs with no scheme or a non‑HTTP scheme
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP/HTTPS URLs are allowed")

    # Reject URLs with missing network location (e.g., "http:///path")
    if not parsed.netloc:
        raise ValueError("URL must contain a host")

    # Validate domain format
    if not DOMAIN_RE.match(parsed.hostname or ""):
        raise ValueError("Malformed hostname")

    # Check against approved domains
    if not _is_approved_domain(parsed.hostname):
        raise ValueError(f"Domain '{parsed.hostname}' is not approved for redirection")

    # Reconstruct the URL to ensure no extra fragments or query parts that might
    # be abused for phishing. We keep path, params, query and fragment as is,
    # but you could strip or sanitize them here if needed.
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        parsed.params,
        parsed.query,
        parsed.fragment
    ))

    return safe_url

# Example usage:
if __name__ == "__main__":
    try:
        print(process_url_redirect("https://example.com/some/path?x=1#frag"))
    except ValueError as e:
        print(f"Invalid URL: {e}")