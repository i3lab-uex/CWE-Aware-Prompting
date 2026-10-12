import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# List of approved providers (exact hostnames or domain suffixes)
APPROVED_HOSTS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",  # Google News
    "rss.cnn.com",
    "feeds.feedburner.com",
    "feeds.reuters.com",
}

# Allow subdomains of the approved hosts
APPROVED_DOMAINS = {
    ".rss.nytimes.com",
    ".feeds.bbci.co.uk",
    ".news.google.com",
    ".rss.cnn.com",
    ".feeds.feedburner.com",
    ".feeds.reuters.com",
}

# Regular expression for detecting private IP ranges
PRIVATE_IP_RE = re.compile(
    r"^(10\.|172\.(1[6-9]|2\d|3[0-1])\.|192\.168\.)"
)

def _is_private_ip(ip: str) -> bool:
    """
    Check if the given IP address string is in a private network.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private
    except ValueError:
        # Not a valid IP address
        return False

def _is_private_hostname(hostname: str) -> bool:
    """
    Resolve the hostname to IP addresses and check if any are private.
    """
    try:
        # Resolve all addresses for the hostname
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        # Hostname could not be resolved; treat as unsafe
        return True

    for info in infos:
        ip = info[4][0]
        if _is_private_ip(ip):
            return True
    return False

def validate_rss_link(rss_link: str) -> str:
    """
    Validate an RSS feed URL, ensuring it comes from a trusted provider
    and does not point to internal or private networks.

    Parameters:
        rss_link (str): The URL of the RSS feed being validated.

    Returns:
        str: A sanitized, normalized feed URL limited to trusted providers.

    Raises:
        ValueError: If the URL is not from an approved provider or points
                    to a restricted internal network.
    """
    if not isinstance(rss_link, str):
        raise ValueError("rss_link must be a string")

    parsed = urlparse(rss_link)

    # Enforce HTTP or HTTPS scheme
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only HTTP and HTTPS schemes are allowed")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Normalize host to lowercase for comparison
    host_lower = host.lower()

    # Check if host is exactly an approved provider or a subdomain
    allowed = (
        host_lower in APPROVED_HOSTS
        or any(host_lower.endswith(domain) for domain in APPROVED_DOMAINS)
    )
    if not allowed:
        raise ValueError(f"Unapproved RSS provider: {host}")

    # Ensure the hostname does not resolve to a private IP
    if _is_private_hostname(host_lower):
        raise ValueError("URL resolves to a private network address")

    # Reconstruct the URL with canonical form (lowercase scheme and netloc)
    sanitized = urlunparse(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            parsed.fragment or "",
        )
    )

    return sanitized