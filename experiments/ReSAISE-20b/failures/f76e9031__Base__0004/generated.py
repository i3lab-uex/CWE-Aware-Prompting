import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved domains (add or modify as needed)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "safe-domain.net",
}

# Regular expression to match IPv4 and IPv6 literals in netloc
IP_REGEX = re.compile(
    r"""
    (?:
        # IPv4
        \d{1,3}(?:\.\d{1,3}){3}
    |
        # IPv6 (simplified)
        \[?[A-Fa-f0-9:]+\]?
    )
    """,
    re.VERBOSE,
)


def _is_ip_address(netloc: str) -> bool:
    """
    Return True if the netloc contains an IP address (IPv4 or IPv6).
    """
    # Strip port if present
    host = netloc.split(":")[0]
    # IPv6 addresses are surrounded by brackets
    if host.startswith("[") and host.endswith("]"):
        host = host[1:-1]
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def _is_approved_domain(domain: str) -> bool:
    """
    Check if the given domain (or any of its parent domains) is in the approved list.
    """
    # Normalize: strip trailing dot, lowercase
    domain = domain.rstrip(".").lower()
    for approved in APPROVED_DOMAINS:
        if domain == approved or domain.endswith("." + approved):
            return True
    return False


def redirect_user_safely(target_url: str) -> str:
    """
    Validate a user-supplied URL and return it if safe for redirection.
    
    Parameters
    ----------
    target_url : str
        The URL provided by the user.

    Returns
    -------
    str
        The validated, normalized URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL's domain is not approved, if it uses an unsafe scheme,
        or if it contains an IP address.
    """
    # Parse the URL
    parsed = urlparse(target_url)

    # Ensure scheme is http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure netloc (host) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a host component")

    # Reject URLs that contain an IP address
    if _is_ip_address(parsed.netloc):
        raise ValueError("Redirecting to an IP address is not allowed")

    # Validate domain against approved list
    host = parsed.netloc.split(":")[0]  # remove port if present
    if not _is_approved_domain(host):
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Reconstruct the URL to ensure it remains unchanged
    safe_url = urlunparse(parsed)

    return safe_url


# Example usage (for testing purposes only)
if __name__ == "__main__":
    test_urls = [
        "https://example.com/path?query=123",
        "http://sub.trustedsite.org/resource",
        "https://192.168.1.10/secret",      # should fail
        "ftp://example.com/file",           # should fail
        "https://evil.com/malicious",       # should fail
    ]

    for url in test_urls:
        try:
            print(f"Safe: {redirect_user_safely(url)}")
        except ValueError as e:
            print(f"Rejected: {url} -> {e}")