import re
import socket
from urllib.parse import urlparse, urlunparse

# List of trusted RSS providers (hostname patterns or full hostnames)
TRUSTED_PROVIDERS = [
    r'^rss\.nytimes\.com$',
    r'^feeds\.bbc\.co\.uk$',
    r'^news\.cnn\.com$',
    r'^rss\.guardian\.com$',
    # Add more trusted provider patterns as needed
]

# Regular expression for private, loopback and link‑local IP ranges (CWE‑918 mitigation)
PRIVATE_IP_REGEX = re.compile(
    r'''
    ^(?:  # start of group
        (?:10\.|192\.168\.)            # 10.x.x.x or 192.168.x.x
        \d{1,3}\.\d{1,3}               # rest of the address
        |
        172\.(?:1[6-9]|2\d|3[0-1])\.    # 172.16–172.31
        \d{1,3}\.\d{1,3}
        |
        127\.0\.0\.1                    # loopback
        |
        ::1                             # IPv6 loopback
    )$
    ''',
    re.VERBOSE,
)

def _is_trusted_hostname(hostname: str) -> bool:
    """Return True if hostname matches a trusted provider pattern."""
    return any(re.match(pattern, hostname) for pattern in TRUSTED_PROVIDERS)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or loopback."""
    return PRIVATE_IP_REGEX.match(ip) is not None

def _resolve_hostname(hostname: str):
    """Resolve the hostname to all associated IP addresses."""
    try:
        # getaddrinfo returns tuples: (family, type, proto, canonname, sockaddr)
        infos = socket.getaddrinfo(hostname, None, family=socket.AF_UNSPEC, proto=socket.IPPROTO_TCP)
        return {info[4][0] for info in infos}
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

def check_rss_source(source_url: str) -> str:
    """
    Validate that the provided RSS feed URL comes from a trusted provider
    and does not point to an internal or private network address.

    Parameters:
        source_url (str): The RSS feed URL to validate.

    Returns:
        str: The original URL if it passes all checks.

    Raises:
        ValueError: If the URL is not from a trusted provider or resolves
                    to an internal/private IP address.
    """
    if not source_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(source_url)

    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}'. Only HTTP/HTTPS allowed.")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL does not contain a valid hostname")

    # 1. Check if the hostname matches a trusted provider
    if not _is_trusted_hostname(hostname):
        raise ValueError(f"Hostname '{hostname}' is not in the list of trusted providers")

    # 2. Resolve hostname and ensure no private IPs are returned
    resolved_ips = _resolve_hostname(hostname)
    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to private IP address {ip}")

    # 3. Reconstruct the URL to ensure it is well‑formed
    sanitized_url = urlunparse(parsed._replace(netloc=hostname))
    return sanitized_url

# Example usage:
if __name__ == "__main__":
    test_urls = [
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "http://feeds.bbci.co.uk/news/world/rss.xml",
        "https://malicious.internal.local/feed.xml",  # should raise ValueError
    ]

    for url in test_urls:
        try:
            result = check_rss_source(url)
            print(f"✅ Valid: {result}")
        except ValueError as e:
            print(f"❌ Invalid: {url} -> {e}")