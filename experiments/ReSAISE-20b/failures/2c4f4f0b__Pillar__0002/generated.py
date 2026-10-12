#!/usr/bin/env python3
"""
check_rss_source.py

Securely validates an RSS feed URL against a whitelist of trusted providers
and ensures the destination is not an internal network address.
"""

import re
import socket
from urllib.parse import urlparse

# --------------------------------------------------------------------------- #
# Trusted providers list – domain names or subdomain patterns.
# Add additional trusted domains as needed.
_TRUSTED_PROVIDERS = {
    r"^rss\.nytimes\.com$",
    r"^feeds\.bbc\.co\.uk$",
    r"^rss\.reuters\.com$",
    r"^news\.cnn\.com$",
    r"^feeds\.guardian\.com$",
}

# Regular expression to detect private IP ranges (RFC 1918, link-local, etc.)
_PRIVATE_IP_REGEX = re.compile(
    r"^(?:"
    # 10.0.0.0/8
    r"(10\.(?:[0-9]{1,3}\.){2}[0-9]{1,3})|"
    # 172.16.0.0/12
    r"(172\.(?:1[6-9]|2[0-9]|3[01])\.[0-9]{1,3}\.[0-9]{1,3})|"
    # 192.168.0.0/16
    r"(192\.168\.[0-9]{1,3}\.[0-9]{1,3})|"
    # 127.0.0.0/8 (loopback)
    r"(127\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})|"
    # 169.254.0.0/16 (link-local)
    r"(169\.254\.[0-9]{1,3}\.[0-9]{1,3})|"
    # IPv6 private addresses (fc00::/7)
    r"(fc[0-9a-f]{1}:[0-9a-f:]+)|"
    r"(fd[0-9a-f]{1}:[0-9a-f:]+)"
    r")$",
    re.IGNORECASE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private or reserved range."""
    # Handle IPv4
    try:
        socket.inet_aton(ip)
    except OSError:
        # Not a valid IPv4 address; try IPv6
        try:
            socket.inet_pton(socket.AF_INET6, ip)
        except OSError:
            return False  # Not a valid IP
    return bool(_PRIVATE_IP_REGEX.match(ip))

def _resolve_hostname(hostname: str) -> list[str]:
    """Return a list of resolved IP addresses for the given hostname."""
    try:
        return socket.gethostbyname_ex(hostname)[2]
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from None

def _is_trusted_domain(domain: str) -> bool:
    """Check if the domain matches any of the trusted provider patterns."""
    for pattern in _TRUSTED_PROVIDERS:
        if re.match(pattern, domain, re.IGNORECASE):
            return True
    return False

def check_rss_source(source_url: str) -> str:
    """
    Validate that the given RSS feed URL originates from a trusted provider
    and does not point to an internal network address.

    Parameters:
        source_url (str): The RSS feed URL to validate.

    Returns:
        str: The validated, trusted URL.

    Raises:
        ValueError: If the URL is malformed, not HTTPS/HTTP,
                    resolves to a private IP, or does not belong
                    to a trusted provider.
    """
    if not isinstance(source_url, str):
        raise ValueError("source_url must be a string")

    parsed = urlparse(source_url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}'. Only HTTP and HTTPS are allowed.")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc).")

    # Normalise domain to lowercase for comparison
    hostname = parsed.hostname.lower()
    if not _is_trusted_domain(hostname):
        raise ValueError(f"Domain '{hostname}' is not in the list of trusted providers.")

    # Resolve hostname to IP(s) and ensure none are private
    for ip in _resolve_hostname(hostname):
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' for domain '{hostname}' is private or reserved.")

    # All checks passed – return the original URL
    return source_url

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Simple demo – replace with real URLs as needed
    test_urls = [
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "http://feeds.bbci.co.uk/news/world/rss.xml",
        "https://example.com/invalid-feed.xml",  # not trusted
    ]

    for url in test_urls:
        try:
            valid = check_rss_source(url)
            print(f"✅ Valid: {valid}")
        except ValueError as err:
            print(f"❌ Invalid: {url} – {err}")