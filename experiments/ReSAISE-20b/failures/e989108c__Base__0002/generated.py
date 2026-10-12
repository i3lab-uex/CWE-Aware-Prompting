import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# Trusted image hosting domains (case‑insensitive)
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trusted.org",
    "assets.safe-host.net",
}

# IP networks that are considered private or otherwise unsafe
UNSAFE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),   # link‑local
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),         # unique local
]

def _is_ip_safe(ip: str) -> bool:
    """Return True if the IP address is not in any unsafe range."""
    try:
        ip_obj = ipaddress.ip_address(ip)
    except ValueError:
        return False
    for net in UNSAFE_IP_RANGES:
        if ip_obj in net:
            return False
    return True

def _resolve_host(host: str) -> bool:
    """Resolve host to IP(s) and ensure all are safe."""
    try:
        # gethostbyname_ex returns (hostname, aliaslist, ipaddrlist)
        _, _, ip_addrs = socket.gethostbyname_ex(host)
    except socket.gaierror:
        return False
    return all(_is_ip_safe(ip) for ip in ip_addrs)

def get_image_link(link_image: str) -> str:
    """
    Validate that the supplied image URL points to a trusted domain and
    resolves to a safe IP address. Return the normalized absolute URL.

    Raises:
        ValueError: If the URL scheme is unsupported, host is not trusted,
                    or DNS resolution points to an unsafe IP.
    """
    if not isinstance(link_image, str):
        raise ValueError("link_image must be a string")

    parsed = urlparse(link_image)

    # Ensure the URL is absolute and uses http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Unsupported URL scheme")

    if not parsed.netloc:
        raise ValueError("URL must contain a host component")

    # Normalize the hostname for comparison
    host = parsed.hostname.lower()
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {host}")

    # Resolve DNS and check for unsafe IPs
    if not _resolve_host(host):
        raise ValueError("DNS resolution points to an unsafe IP address")

    # Rebuild the URL ensuring consistent formatting
    normalized = urlunparse((
        parsed.scheme,
        parsed.netloc.lower(),
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or "",
    ))
    return normalized