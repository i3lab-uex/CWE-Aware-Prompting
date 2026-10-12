import re
import socket
from urllib.parse import urlparse, urlunparse

# ----------------------------------------------------------------------
# Trusted domain configuration – add any external API domains you wish
# to allow.  Use fully qualified domain names or regular expressions.
# ----------------------------------------------------------------------
TRUSTED_DOMAINS = [
    re.compile(r"^api\.example\.com$"),
    re.compile(r"^service\.trustedprovider\.org$"),
]

# ----------------------------------------------------------------------
# Private IP address ranges that must never be reachable from the public
# internet.  These are defined according to RFC1918, RFC4193 and RFC5735.
# ----------------------------------------------------------------------
PRIVATE_IP_RANGES = [
    ("10.0.0.0", "10.255.255.255"),
    ("172.16.0.0", "172.31.255.255"),
    ("192.168.0.0", "192.168.255.255"),
    ("127.0.0.0", "127.255.255.255"),   # loopback
    ("169.254.0.0", "169.254.255.255"), # link-local
    ("::1", "::1"),                     # IPv6 loopback
    ("fc00::", "fdff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"), # IPv6 unique local
]

def _ip_in_range(ip_addr, start_ip, end_ip):
    """Return True if ip_addr is within the inclusive range [start_ip, end_ip]."""
    # IPv4
    if ":" not in start_ip:
        ip = int.from_bytes(socket.inet_aton(ip_addr), "big")
        start = int.from_bytes(socket.inet_aton(start_ip), "big")
        end = int.from_bytes(socket.inet_aton(end_ip), "big")
        return start <= ip <= end
    # IPv6
    ip = int.from_bytes(socket.inet_pton(socket.AF_INET6, ip_addr), "big")
    start = int.from_bytes(socket.inet_pton(socket.AF_INET6, start_ip), "big")
    end = int.from_bytes(socket.inet_pton(socket.AF_INET6, end_ip), "big")
    return start <= ip <= end

def _is_private_ip(ip_addr):
    """Check if the given IP address is part of a private network."""
    for start, end in PRIVATE_IP_RANGES:
        if _ip_in_range(ip_addr, start, end):
            return True
    return False

def inspect_api_url(url_to_inspect: str) -> str:
    """
    Validate that the supplied URL points to an external, trusted API.

    Parameters
    ----------
    url_to_inspect : str
        The URL to be validated.

    Returns
    -------
    str
        The same URL if it is considered safe for external API use.

    Raises
    ------
    ValueError
        If the URL does not belong to a trusted domain or resolves to a private IP.
    """
    # 1. Basic URL parsing
    parsed = urlparse(url_to_inspect)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {url_to_inspect}")

    # 2. Enforce https for external API calls
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed for external API calls")

    # 3. Check against trusted domain list
    host = parsed.hostname.lower()
    if not any(regex.match(host) for regex in TRUSTED_DOMAINS):
        raise ValueError(f"Domain '{host}' is not trusted")

    # 4. Resolve the hostname to IP(s) and ensure none are private
    try:
        addr_info = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve host '{host}': {exc}") from exc

    for entry in addr_info:
        family, _, _, _, sockaddr = entry
        ip_addr = sockaddr[0]
        if _is_private_ip(ip_addr):
            raise ValueError(f"Resolved IP {ip_addr} is private; access denied")

    # 5. Reconstruct the URL to avoid any hidden path manipulations
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        parsed.query,  # preserve query parameters as-is
        ""   # fragment
    ))

    return sanitized

# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     try:
#         safe_url = inspect_api_url("https://api.example.com/v1/data?token=abc")
#         print(f"Safe URL: {safe_url}")
#     except ValueError as e:
#         print(f"URL validation failed: {e}")