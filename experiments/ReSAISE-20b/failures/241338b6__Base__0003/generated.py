import re
import socket
from urllib.parse import urlparse
from ipaddress import ip_address, ip_network

# --------------------------------------------------------------------
# Whitelisted external API domains (add or remove as needed)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "api.service.net",
    "openweathermap.org",
    # ... other approved domains
}

# Private IP networks that must be blocked (CVE-2018-1337 style)
PRIVATE_IP_RANGES = [
    ip_network("10.0.0.0/8"),
    ip_network("172.16.0.0/12"),
    ip_network("192.168.0.0/16"),
    ip_network("127.0.0.0/8"),      # loopback
    ip_network("169.254.0.0/16"),   # link local
    ip_network("::1/128"),          # IPv6 loopback
]

# --------------------------------------------------------------------
def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is within a private or reserved range."""
    try:
        addr = ip_address(ip)
    except ValueError:
        # Invalid IP address
        return True
    for net in PRIVATE_IP_RANGES:
        if addr in net:
            return True
    return False

def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve a hostname to its IP addresses (both IPv4 & IPv6)."""
    try:
        return socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return []

def verify_api_link(url_to_check: str) -> str:
    """
    Validate that the provided URL points to an approved external API.

    Parameters
    ----------
    url_to_check : str
        The URL to be validated.

    Returns
    -------
    str
        The original URL if it is approved and safe to use.

    Raises
    ------
    ValueError
        If the URL is not in the whitelist or resolves to a private IP.
    """
    # Basic parsing
    parsed = urlparse(url_to_check)
    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("URL must use http or https scheme")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # 1. Check against the whitelist
    if hostname.lower() not in WHITELISTED_DOMAINS:
        # Allow subdomains of whitelisted domains? If needed, adjust logic
        raise ValueError(f"Hostname '{hostname}' is not an approved domain")

    # 2. Resolve hostname to IP addresses
    addrinfo_list = _resolve_hostname(hostname)
    if not addrinfo_list:
        raise ValueError(f"Could not resolve hostname '{hostname}'")

    # 3. Ensure none of the resolved IPs are private
    for family, _, _, _, sockaddr in addrinfo_list:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to private IP {ip}")

    # 4. Additional sanity checks (optional)
    # Example: disallow URLs containing IPv6 literal addresses directly
    if re.search(r"\[.*\]", parsed.netloc):
        raise ValueError("IPv6 literal addresses are not allowed")

    # If all checks pass, return the original URL
    return url_to_check

# --------------------------------------------------------------------
# Example usage (uncomment to test)
# try:
#     safe_url = verify_api_link("https://api.example.com/data")
#     print(f"Approved URL: {safe_url}")
# except ValueError as e:
#     print(f"URL rejected: {e}")