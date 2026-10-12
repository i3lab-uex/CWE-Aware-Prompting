import re
from urllib.parse import urlparse, urlunparse
import socket

# List of approved RSS providers (add or remove as needed)
APPROVED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",   # Google News RSS
    "rss.cnn.com",
    "feeds.reuters.com",
}

# Regex for private IP ranges (CVE-2023-... and similar)
PRIVATE_IP_RANGES = [
    re.compile(r"^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^172\.1[6-9]\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^172\.2[0-9]\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^172\.3[0-1]\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^192\.168\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^127\.\d{1,3}\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^169\.254\.\d{1,3}\.\d{1,3}$"),
]

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private / reserved range."""
    for pattern in PRIVATE_IP_RANGES:
        if pattern.match(ip):
            return True
    return False

def _resolve_hostname(hostname: str) -> list[str]:
    """Return a list of IP addresses for the hostname."""
    try:
        return socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return []

def check_rss_address(rss_address: str) -> str:
    """
    Validate an RSS feed URL against a whitelist of trusted providers
    and ensure it does not resolve to a private or internal IP address.

    Parameters:
        rss_address (str): The RSS feed URL to validate.

    Returns:
        str: A sanitized and validated RSS feed URL.

    Raises:
        ValueError: If the URL is not from an approved provider,
                    uses a disallowed scheme, or resolves to a private IP.
    """
    # Parse the URL and validate scheme
    parsed = urlparse(rss_address)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http/https are allowed.")

    # Normalise hostname (lowercase, strip port)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname.")

    # Check against approved domains
    if host.lower() not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not an approved RSS provider.")

    # Resolve hostname to IPs and ensure none are private
    addr_info = _resolve_hostname(host)
    if not addr_info:
        raise ValueError(f"Could not resolve hostname '{host}'.")

    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' for host '{host}' is private or restricted.")

    # Reconstruct the URL with only scheme, netloc and path (remove fragments)
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        "",  # params
        parsed.query,
        ""   # fragment
    ))
    return sanitized

# Example usage (uncomment for testing):
# try:
#     url = check_rss_address("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
#     print("Validated URL:", url)
# except ValueError as e:
#     print("Validation failed:", e)