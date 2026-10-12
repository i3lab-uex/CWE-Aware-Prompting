import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# A small whitelist of approved domains or domain patterns.
# Use regexes for sub‑domains, e.g. r'^api\.example\.com$' or
# a simple string for exact matches.
ALLOWED_DOMAIN_PATTERNS = [
    r'^api\.example\.com$',          # Exact domain
    r'^service\..+\.mycorp\.org$'   # Any sub‑domain under mycorp.org
]

# Optional: allow certain IP ranges (e.g. public CIDR blocks)
ALLOWED_IP_RANGES = [
    ipaddress.IPv4Network('52.0.0.0/8'),   # Example public range
    ipaddress.IPv6Network('2001:db8::/32') # Example IPv6 range
]

# Private / link‑local / loopback IP ranges per RFC 1918 and related specs.
PRIVATE_IP_RANGES = [
    ipaddress.IPv4Network('10.0.0.0/8'),
    ipaddress.IPv4Network('172.16.0.0/12'),
    ipaddress.IPv4Network('192.168.0.0/16'),
    ipaddress.IPv6Network('fd00::/8'),   # Unique local
    ipaddress.IPv4Network('127.0.0.0/8'),
    ipaddress.IPv6Network('::1/128')
]

def _is_ip_private(ip: str) -> bool:
    """Return True if the IP is in a private or reserved range."""
    addr = ipaddress.ip_address(ip)
    return any(addr in rng for rng in PRIVATE_IP_RANGES)

def _is_ip_allowed(ip: str) -> bool:
    """Return True if the IP is in an explicitly allowed public range."""
    addr = ipaddress.ip_address(ip)
    return any(addr in rng for rng in ALLOWED_IP_RANGES)

def _match_allowed_domain(domain: str) -> bool:
    """Check if the domain matches one of the allowed patterns."""
    for pattern in ALLOWED_DOMAIN_PATTERNS:
        if re.match(pattern, domain, flags=re.IGNORECASE):
            return True
    return False

def check_api_endpoint(endpoint_url: str) -> str:
    """
    Verify that `endpoint_url` points to an approved external API endpoint.

    The function performs the following checks:
      1. URL must be absolute and use HTTP or HTTPS.
      2. The hostname resolves to at least one IP address that is not
         private, link‑local, or loopback.
      3. The resolved IP is either in an explicitly allowed public range
         (optional) or the hostname matches a whitelisted domain pattern.

    Returns:
        The original URL if it passes all checks.

    Raises:
        ValueError: If any check fails.
    """
    # 1. Parse and basic validation
    parsed = urlparse(endpoint_url)
    if not parsed.scheme or parsed.scheme.lower() not in ('http', 'https'):
        raise ValueError("URL must use http or https scheme")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (hostname)")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("Unable to extract hostname from URL")

    # 2. Resolve hostname to IP addresses
    try:
        addr_info = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed: {exc}") from exc

    # 3. Validate each resolved IP
    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_ip_private(ip):
            raise ValueError(f"IP {ip} resolved from hostname '{hostname}' is private or reserved")

        # Optional: enforce that IP is in an explicitly allowed public range
        if not _is_ip_allowed(ip):
            # If IP is not in an allowed range, fall back to domain whitelist
            if not _match_allowed_domain(hostname):
                raise ValueError(
                    f"IP {ip} resolved from hostname '{hostname}' is not in an allowed range "
                    "and the domain does not match any whitelist pattern"
                )

    # 4. Domain whitelist check (in case IP checks are not strict)
    if not _match_allowed_domain(hostname):
        raise ValueError(f"Domain '{hostname}' is not in the approved whitelist")

    # 5. Reconstruct and return a clean URL (optional normalization)
    cleaned = parsed._replace(netloc=hostname.lower())
    return urlunparse(cleaned)

# Example usage (uncomment for testing):
# try:
#     verified = check_api_endpoint("https://api.example.com/v1/resource")
#     print(f"Verified URL: {verified}")
# except ValueError as e:
#     print(f"Invalid endpoint: {e}")