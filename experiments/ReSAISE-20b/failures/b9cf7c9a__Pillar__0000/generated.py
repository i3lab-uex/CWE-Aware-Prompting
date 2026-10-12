import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# --------------------------------------------------------------------------- #
# Configuration: list of approved domains (wildcards allowed with simple regex)
# --------------------------------------------------------------------------- #
APPROVED_DOMAIN_PATTERNS = [
    r"^api\.example\.com$",          # exact match
    r"^service\.trusted\.org$",     # exact match
    r"^api\.example\.com\.[a-z]{2}$",  # subdomains of example.com
]

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _is_approved_domain(host: str) -> bool:
    """Return True if host matches one of the approved domain patterns."""
    for pattern in APPROVED_DOMAIN_PATTERNS:
        if re.match(pattern, host, flags=re.IGNORECASE):
            return True
    return False


def _is_internal_ip(ip: str) -> bool:
    """Return True if the given IP string is a private or reserved address."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_reserved
    except ValueError:
        # Not a valid IP address
        return False


def _resolve_host(host: str) -> list[str]:
    """Return a list of IP addresses for the given host."""
    try:
        return [info[4][0] for info in socket.getaddrinfo(host, None)]
    except socket.gaierror:
        return []


# --------------------------------------------------------------------------- #
# Main validation function
# --------------------------------------------------------------------------- #
def check_api_url(endpoint_url: str) -> str:
    """
    Validate that the supplied URL points to an approved external API.

    Parameters
    ----------
    endpoint_url : str
        The URL to validate.

    Returns
    -------
    str
        A canonicalized version of the input URL that has been validated.

    Raises
    ------
    ValueError
        If the URL does not belong to an approved domain, or if it resolves
        to a private/internal IP address.
    """
    # Basic parsing and scheme check
    parsed = urlparse(endpoint_url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme: {parsed.scheme!r}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # 1. Check domain against approved patterns
    if not _is_approved_domain(host):
        raise ValueError(f"Domain {host!r} is not in the approved list")

    # 2. Resolve host to IP addresses and ensure none are internal
    ips = _resolve_host(host)
    if not ips:
        raise ValueError(f"Could not resolve host: {host!r}")

    for ip in ips:
        if _is_internal_ip(ip):
            raise ValueError(f"Resolved IP {ip!r} is internal or reserved")

    # 3. Reconstruct a normalized URL (remove userinfo, fragments, etc.)
    netloc = host
    if parsed.port:
        netloc += f":{parsed.port}"
    canonical_url = urlunparse((
        parsed.scheme,
        netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # strip fragment
    ))
    return canonical_url


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     try:
#         url = check_api_url("https://api.example.com/v1/resource")
#         print(f"Validated URL: {url}")
#     except ValueError as exc:
#         print(f"Validation failed: {exc}")