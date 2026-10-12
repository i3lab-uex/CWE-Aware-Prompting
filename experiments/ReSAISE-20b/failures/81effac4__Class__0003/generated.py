import re
import socket
from urllib.parse import urlparse, urlunparse

# A simple whitelist of trusted domains. Extend this list as needed.
TRUSTED_DOMAINS = {
    "api.example.com",
    "data.provider.org",
    "service.company.net",
}

# Regex to detect private / reserved IP ranges
PRIVATE_IP_RANGES = re.compile(
    r"^(?:"
    r"(10\.\d{1,3}\.\d{1,3}\.\d{1,3})|"          # 10.0.0.0/8
    r"(172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|"  # 172.16.0.0/12
    r"(192\.168\.\d{1,3}\.\d{1,3})|"              # 192.168.0.0/16
    r"(169\.254\.\d{1,3}\.\d{1,3})|"              # 169.254.0.0/16
    r"(127\.\d{1,3}\.\d{1,3}\.\d{1,3})|"           # 127.0.0.0/8
    r"(::1)|"                                     # IPv6 loopback
    r"fe80:(?:[0-9a-f]{1,4}:){0,7}[0-9a-f]{1,4}"   # IPv6 link-local
    r")$",
    re.IGNORECASE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private or reserved range."""
    return bool(PRIVATE_IP_RANGES.match(ip))

def _resolve_host(host: str) -> list[str]:
    """Return a list of IP addresses for the given host."""
    try:
        infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return []
    return [info[4][0] for info in infos]

def check_api_link(api_link: str) -> str:
    """
    Validate that the supplied API link points to an external, trusted endpoint.

    Args:
        api_link: The URL string to validate.

    Returns:
        A normalized, validated URL.

    Raises:
        ValueError: If the URL is malformed, uses an unsupported scheme,
                    points to a private IP address, or does not belong
                    to the trusted domain list.
    """
    if not isinstance(api_link, str):
        raise ValueError("api_link must be a string")

    parsed = urlparse(api_link)

    # Ensure we have http/https scheme
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http and https are allowed.")

    # Host must be present
    if not parsed.hostname:
        raise ValueError("URL does not contain a hostname")

    # Verify domain against whitelist
    host = parsed.hostname.lower()
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not trusted")

    # Resolve hostname to IP addresses
    ips = _resolve_host(host)
    if not ips:
        raise ValueError(f"Could not resolve hostname '{host}'")

    # Ensure none of the resolved IPs are private or reserved
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' for host '{host}' is in a private or reserved range")

    # Reconstruct the URL to ensure normalization
    normalized = urlunparse((
        parsed.scheme,
        f"{host}{':' + str(parsed.port) if parsed.port else ''}",
        parsed.path or "/",
        "",  # params
        parsed.query,
        ""   # fragment
    ))
    return normalized

# Example usage (uncomment to test):
# try:
#     url = check_api_link("https://api.example.com/v1/data")
#     print(f"Validated URL: {url}")
# except ValueError as e:
#     print(f"Validation failed: {e}")