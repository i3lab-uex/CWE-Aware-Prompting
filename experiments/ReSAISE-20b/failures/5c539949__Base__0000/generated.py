import re
from urllib.parse import urlparse, ParseResult
import ipaddress

# --------------------------------------------------------------------------- #
# Approved domains (and optional subdomains) that the application is allowed to
# redirect users to.  Each entry can be either:
#
#   * a full domain name, e.g. "example.com"
#   * a wildcard subdomain pattern, e.g. "*.trusted.com" (matches any sub‑
#     domain of trusted.com)
#
# The list can be extended or read from a configuration file as needed.
# --------------------------------------------------------------------------- #
APPROVED_DOMAINS = [
    "example.com",
    "*.trusted.com",   # allows foo.trusted.com, bar.baz.trusted.com, etc.
    "safe.org",
]

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_ip_address(host: str) -> bool:
    """Return True if host is a valid IPv4 or IPv6 address."""
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def _normalize_domain(domain: str) -> str:
    """Return the domain in lower case and without trailing dot."""
    return domain.lower().rstrip(".")


def _match_approved_domain(host: str) -> bool:
    """
    Check whether the host matches one of the approved domain patterns.
    Wildcards are supported only at the leftmost label (e.g. *.example.com).
    """
    host = _normalize_domain(host)

    # Reject plain IP addresses (unless explicitly approved)
    if _is_ip_address(host):
        return False

    for pattern in APPROVED_DOMAINS:
        pattern = _normalize_domain(pattern)
        if pattern.startswith("*."):
            # wildcard match: host must end with the domain part after '*.'
            suffix = pattern[2:]  # remove "*."
            if host == suffix or host.endswith("." + suffix):
                return True
        else:
            # exact match
            if host == pattern:
                return True

    return False


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def secure_redirect_handler(redirect_url: str) -> str:
    """
    Validate a user supplied URL and return it only if its domain is approved.

    Parameters
    ----------
    redirect_url : str
        The URL supplied by the user.  It may contain a scheme, host,
        port, path, query string and fragment.

    Returns
    -------
    str
        The validated URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL's domain is not part of the approved list or if it uses an
        unsupported scheme.
    """
    if not isinstance(redirect_url, str):
        raise ValueError("redirect_url must be a string")

    # Parse the URL
    parsed: ParseResult = urlparse(redirect_url)

    # Ensure scheme is http or https
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure a host is present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (host)")

    # Extract host part, ignoring port
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Validate the domain
    if not _match_approved_domain(host):
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Reconstruct the URL to ensure it remains unchanged but sanitized
    safe_url = parsed.geturl()
    return safe_url


# --------------------------------------------------------------------------- #
# Example usage (for demonstration; remove or guard with `if __name__ == "__main__":` in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_urls = [
        "https://example.com/welcome",
        "http://foo.trusted.com/path?x=1#frag",
        "https://unapproved.com",
        "http://192.168.0.1",
    ]

    for url in test_urls:
        try:
            print(f"Redirecting to: {secure_redirect_handler(url)}")
        except ValueError as e:
            print(f"Rejected '{url}': {e}")