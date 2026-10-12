import re
import socket
import ipaddress
from urllib.parse import urlparse

# --------------------------------------------------------------------------- #
#  Whitelist of public API endpoints that are allowed to be called internally.
#  Each entry may contain a domain (e.g. "api.example.com") or an IP
#  address / CIDR block. Wildcards (*) are supported for subdomains.
# --------------------------------------------------------------------------- #
WHITELIST = [
    "api.example.com",
    "*.public-api.org",
    "192.0.2.0/24",          # Example public IP block
    "203.0.113.42",          # Specific public IP
]

# --------------------------------------------------------------------------- #
#  Helper functions
# --------------------------------------------------------------------------- #

def _is_ip_address(host: str) -> bool:
    """Return True if the host is an IP address (IPv4 or IPv6)."""
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False

def _is_internal_ip(ip: str) -> bool:
    """Return True if the IP is in a private, loopback or link-local range."""
    addr = ipaddress.ip_address(ip)
    return (
        addr.is_private or
        addr.is_loopback or
        addr.is_link_local or
        addr.is_reserved or
        addr.is_multicast
    )

def _match_whitelist(host: str) -> bool:
    """Check if the host matches any entry in the WHITELIST."""
    # Resolve host to IPs
    try:
        ips = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return False  # Host could not be resolved

    host_ips = {addr[4][0] for addr in ips}

    # Check each whitelist entry
    for pattern in WHITELIST:
        if pattern.startswith("*."):
            # Wildcard subdomain match
            base = pattern[2:]
            if host.endswith(base):
                return True
        elif "/" in pattern:
            # CIDR block
            net = ipaddress.ip_network(pattern, strict=False)
            if any(net.overlaps(ipaddress.ip_network(f"{ip}/32")) for ip in host_ips):
                return True
        else:
            # Exact domain or IP match
            if pattern == host:
                return True
    return False

# --------------------------------------------------------------------------- #
#  Main function
# --------------------------------------------------------------------------- #

def verify_webhook(webhook_endpoint: str) -> str:
    """
    Validate a webhook URL before it is used to initiate an internal API call.

    Parameters
    ----------
    webhook_endpoint : str
        The external webhook URL provided by an upstream component.

    Returns
    -------
    str
        A validated and secure URL that can be safely used internally.

    Raises
    ------
    ValueError
        If the URL's domain is not in the approved whitelist or if it resolves to an internal/private IP.
    """
    # Basic URL parsing
    parsed = urlparse(webhook_endpoint)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL")

    # Extract hostname (strip port if present)
    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a hostname")

    # Resolve to IP addresses
    try:
        addrinfo = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve hostname '{host}': {exc}") from exc

    ips = {info[4][0] for info in addrinfo}

    # Check that none of the resolved IPs are internal
    if any(_is_internal_ip(ip) for ip in ips):
        raise ValueError("URL resolves to an internal/private IP address")

    # Ensure host matches whitelist
    if not _match_whitelist(host):
        raise ValueError("Domain is not in the approved whitelist")

    # Reconstruct a safe URL (normalise scheme and netloc)
    safe_url = parsed._replace(scheme=parsed.scheme.lower(), netloc=host).geturl()

    return safe_url

# --------------------------------------------------------------------------- #
#  Example usage (for testing only, remove in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/webhook",
        "http://sub.public-api.org/notify",
        "https://192.0.2.5/callback",
        "http://localhost:8000/hook",          # Should fail
        "https://malicious.com/attack"         # Should fail
    ]

    for url in test_urls:
        try:
            print(f"Validating: {url}")
            print(" -> Safe URL:", verify_webhook(url))
        except ValueError as e:
            print(f" -> Validation failed: {e}")
        print("-" * 60)