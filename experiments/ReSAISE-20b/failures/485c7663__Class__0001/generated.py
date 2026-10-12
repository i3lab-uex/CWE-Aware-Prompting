import re
import socket
from urllib.parse import urlparse, unquote_plus
from ipaddress import ip_address, IPv4Address, IPv6Address

# List of domains that are allowed to be called by the system.
# In a real project this list would come from configuration or
# environment variables rather than being hard‑coded.
APPROVED_DOMAINS = {
    "api.example.com",
    "service.company.org",
    "trusted.api.net",
}

# Regular expression for detecting private IP ranges (IPv4 & IPv6)
PRIVATE_IP_RANGES = [
    ("10.0.0.0", "10.255.255.255"),
    ("172.16.0.0", "172.31.255.255"),
    ("192.168.0.0", "192.168.255.255"),
    ("127.0.0.1", "127.255.255.255"),  # loopback
    ("::1", "::1"),
    ("fc00::", "fdff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"),  # unique local
    ("fe80::", "febf:ffff:ffff:ffff:ffff:ffff:ffff:ffff"),  # link local
]

def _is_private_ip(ip: str) -> bool:
    """Return True if ip is in a private or reserved range."""
    try:
        addr = ip_address(ip)
    except ValueError:
        return False  # Not a valid IP address

    for start, end in PRIVATE_IP_RANGES:
        if ip_address(start) <= addr <= ip_address(end):
            return True
    return False

def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve a hostname to its IP addresses.
    Returns a list of IPv4/IPv6 address strings.
    """
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed for {hostname!r}: {exc}") from exc

    return list({info[4][0] for info in infos})  # deduplicate

def enforce_api_security(api_endpoint: str) -> str:
    """
    Verify that a given API endpoint is safe to call.

    The function checks the following:
      * URL uses HTTPS.
      * Hostname is in the approved domain list.
      * The hostname does not resolve to any private or loopback IP addresses.

    Parameters
    ----------
    api_endpoint : str
        The URL that needs to be verified.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, not HTTPS, uses an unapproved domain,
        or resolves to a private/loopback IP address.
    """
    if not api_endpoint:
        raise ValueError("API endpoint must be a non-empty string")

    # Parse URL and validate scheme
    parsed = urlparse(api_endpoint)
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # Validate hostname
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL does not contain a valid hostname")

    # Normalize host for domain comparison
    normalized = hostname.lower()

    if normalized not in APPROVED_DOMAINS:
        raise ValueError(f"Domain {normalized!r} is not in the approved list")

    # Resolve hostname to IPs and ensure none are private
    ip_list = _resolve_hostname(normalized)
    for ip in ip_list:
        if _is_private_ip(ip):
            raise ValueError(
                f"Resolved IP {ip} for host {normalized!r} is private or reserved"
            )

    # Basic sanity check: ensure path/query do not contain suspicious patterns
    # (e.g., references to local file system). This is optional but helps guard against
    # simple SSRF tricks that rely on URL path encoding.
    if re.search(r"(?i)file://", parsed.path):
        raise ValueError("URL path contains forbidden scheme 'file'")

    # All checks passed; return the original URL
    return api_endpoint