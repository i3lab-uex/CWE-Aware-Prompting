import socket
from urllib.parse import urlparse, urlunparse

# A simple whitelist of approved API domains.
ALLOWED_DOMAINS = {
    "api.openai.com",
    "api.github.com",
    "api.example.org",  # add more trusted domains here
}

# IPv4 and IPv6 private, loopback, link‑local ranges to block.
PRIVATE_IP_RANGES = [
    ("10.0.0.0", "10.255.255.255"),
    ("172.16.0.0", "172.31.255.255"),
    ("192.168.0.0", "192.168.255.255"),
    ("127.0.0.0", "127.255.255.255"),   # loopback
    ("169.254.0.0", "169.254.255.255"), # link local
    ("::1", "::1"),
    ("fc00::", "fdff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"),  # unique local
]

def _ip_in_range(ip_addr, start_ip, end_ip):
    """Return True if ip_addr is between start_ip and end_ip (inclusive)."""
    return socket.inet_aton(ip_addr) >= socket.inet_aton(start_ip) and \
           socket.inet_aton(ip_addr) <= socket.inet_aton(end_ip)

def _is_private_ip(host):
    """Check if host resolves to a private IP address."""
    try:
        # Resolve all IPv4 addresses for the hostname
        ip_list = socket.getaddrinfo(host, None, family=socket.AF_INET)
    except socket.gaierror:
        return False  # If resolution fails, treat as non‑private (let caller handle)
    for _, _, _, _, sockaddr in ip_list:
        ip = sockaddr[0]
        for start, end in PRIVATE_IP_RANGES[:5]:  # IPv4 ranges
            if _ip_in_range(ip, start, end):
                return True
    # Resolve IPv6 addresses
    try:
        ip_list = socket.getaddrinfo(host, None, family=socket.AF_INET6)
    except socket.gaierror:
        return False
    for _, _, _, _, sockaddr in ip_list:
        ip = sockaddr[0]
        # IPv6 private ranges are handled via string comparison
        if start <= ip <= end:
            return True
    return False

def verify_api_link(url_to_check: str) -> str:
    """
    Validate that the given URL points to an approved external API.
    
    Parameters
    ----------
    url_to_check : str
        The URL to be validated.

    Returns
    -------
    str
        A normalized URL that has been confirmed to point to an approved external API.

    Raises
    ------
    ValueError
        If the URL does not belong to an approved domain or if it targets internal network addresses.
    """
    parsed = urlparse(url_to_check)

    # Basic scheme check
    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL must use http or https scheme")

    # Ensure a host is present
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Check against the whitelist
    if parsed.hostname.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{parsed.hostname}' is not in the approved list")

    # Prevent SSRF by rejecting internal IPs
    if _is_private_ip(parsed.hostname):
        raise ValueError("URL resolves to a private or internal IP address")

    # Re‑build the URL to ensure it is normalized
    cleaned = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        parsed.params,
        parsed.query,
        parsed.fragment
    ))
    return cleaned