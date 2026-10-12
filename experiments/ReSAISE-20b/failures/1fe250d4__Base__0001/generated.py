import re
import socket
from urllib.parse import urlparse, unquote
import ipaddress

# List of allowed top‑level domains or patterns if needed.
# For a stricter policy you can add entries such as r"^api\.example\.com$".
ALLOWED_DOMAIN_PATTERNS = []  # Empty means any external domain is accepted

# Regular expression to detect obvious internal hostnames
_INTERNAL_HOSTNAME_RE = re.compile(
    r"^(localhost|127\.0\.0\.1|::1)$",
    re.IGNORECASE
)

def _is_internal_ip(ip: str) -> bool:
    """
    Return True if the given IP address string is in a private, loopback,
    link‑local, or other non‑public range.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return (
            addr.is_loopback or
            addr.is_private or
            addr.is_link_local or
            addr.is_reserved or
            addr.is_multicast or
            addr.is_unspecified
        )
    except ValueError:
        # Not a valid IP address
        return True

def _is_allowed_domain(hostname: str) -> bool:
    """
    Check if the hostname matches any of the allowed domain patterns.
    If no patterns are defined, return True (i.e., all external domains allowed).
    """
    if not ALLOWED_DOMAIN_PATTERNS:
        return True
    for pattern in ALLOWED_DOMAIN_PATTERNS:
        if re.match(pattern, hostname):
            return True
    return False

def check_api_endpoint(endpoint_url: str) -> str:
    """
    Validate that the supplied URL points to an external, non‑internal
    network address and uses http/https scheme.

    Parameters
    ----------
    endpoint_url : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it passes validation.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        resolves to a private/internal IP address,
        or points to an unapproved domain.
    """
    if not isinstance(endpoint_url, str):
        raise ValueError("endpoint_url must be a string")

    parsed = urlparse(endpoint_url)
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http and https are allowed.")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Reject obvious internal hostnames
    if _INTERNAL_HOSTNAME_RE.match(hostname):
        raise ValueError(f"Hostname '{hostname}' is disallowed (internal).")

    # DNS resolution
    try:
        addrinfo = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

    # Verify that at least one resolved IP is external
    for _, _, _, _, sockaddr in addrinfo:
        ip = sockaddr[0]
        if not _is_internal_ip(ip):
            break
    else:
        raise ValueError(f"All resolved IP addresses for '{hostname}' are internal or private.")

    # Optional domain whitelist check
    if not _is_allowed_domain(hostname):
        raise ValueError(f"Domain '{hostname}' is not in the list of allowed domains.")

    # All checks passed
    return endpoint_url

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     try:
#         print(check_api_endpoint("https://api.github.com/repos"))
#     except ValueError as e:
#         print(f"Invalid endpoint: {e}")