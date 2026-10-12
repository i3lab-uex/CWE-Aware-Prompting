import re
import socket
from urllib.parse import urlparse, urlunparse

# List of domains that are considered safe for redirection
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "secure.example.net",
}

# Regex to detect IP addresses
IP_RE = re.compile(r"""
    ^
    (?:
      # IPv4
      (?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)
      \.
    ){3}
    (?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)
    $
""", re.VERBOSE)


def _is_ip_address(host: str) -> bool:
    """Return True if host is an IP address."""
    return bool(IP_RE.match(host))


def _is_private_ip(ip: str) -> bool:
    """Check if an IP address is in a private, loopback or reserved range."""
    # Convert to integer for comparison
    parts = [int(p) for p in ip.split('.')]
    a, b, c, d = parts

    # 10.0.0.0/8
    if a == 10:
        return True
    # 172.16.0.0/12
    if a == 172 and 16 <= b <= 31:
        return True
    # 192.168.0.0/16
    if a == 192 and b == 168:
        return True
    # 127.0.0.0/8 (loopback)
    if a == 127:
        return True
    # 169.254.0.0/16 (link-local)
    if a == 169 and b == 254:
        return True
    # Reserved addresses (0.0.0.0/8, 255.255.255.255)
    if a == 0 or ip == "255.255.255.255":
        return True
    return False


def _resolve_host(host: str) -> list[str]:
    """Resolve a hostname to all IPv4 addresses."""
    try:
        return [info[4][0] for info in socket.getaddrinfo(host, None, socket.AF_INET)]
    except socket.gaierror:
        return []


def redirect_user_safely(target_url: str) -> str:
    """
    Validate a user supplied URL and return it if it is safe for redirection.

    The function ensures:
      * Only http or https schemes are allowed.
      * The host is in the list of approved domains.
      * The host does not resolve to a private or reserved IP address.

    Raises:
        ValueError: If the URL is not safe for redirection.
    """
    if not isinstance(target_url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(target_url)

    # Scheme must be http or https
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError("Only http and https schemes are allowed")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Normalize to lowercase for domain comparison
    host_lower = host.lower()

    # Check if the hostname is an IP address; reject private/reserved IPs
    if _is_ip_address(host_lower):
        if _is_private_ip(host_lower):
            raise ValueError("Redirect to private IP addresses is forbidden")
        # No domain whitelist check for plain IPs – they are not allowed
        raise ValueError("Redirect to arbitrary IP addresses is forbidden")

    # Ensure the hostname ends with an approved domain
    if not any(host_lower == domain or host_lower.endswith("." + domain) for domain in APPROVED_DOMAINS):
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Resolve the hostname and ensure it doesn't point to a private IP
    resolved_ips = _resolve_host(host_lower)
    if not resolved_ips:
        raise ValueError(f"Could not resolve hostname '{host}'")
    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{host}' resolves to private IP address {ip}")

    # Reconstruct the URL to ensure consistency
    safe_url = urlunparse(parsed._replace(netloc=parsed.netloc.lower()))
    return safe_url