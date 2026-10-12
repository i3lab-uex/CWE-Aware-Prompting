#!/usr/bin/env python3
"""
Utility to validate RSS feed URLs against a whitelist of trusted providers.

The function checks that:
1. The URL uses an allowed scheme (http or https).
2. The hostname resolves to a public IP address and is not in
   private/reserved ranges (CVE/CWE-918 mitigation).
3. The hostname is in a pre‑defined whitelist of trusted RSS providers.

If any check fails, a ValueError is raised.
"""

import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# ----------------------------------------------------------------------
# Configuration: List of trusted RSS providers (hostnames or regex patterns)
# ----------------------------------------------------------------------
TRUSTED_HOSTS = [
    r"^rss\.nytimes\.com$",
    r"^feeds\.bbc\.co\.uk$",
    r"^rss\.guardian\.com$",
    r"^news\.ap.org$",
    r"^feedproxy\.google\.com$",
    # Add more trusted domains or regex patterns here
]

# Compile the regexes for performance
TRUSTED_HOSTS_RE = [re.compile(pattern, re.IGNORECASE) for pattern in TRUSTED_HOSTS]

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _is_trusted_host(host: str) -> bool:
    """Return True if the host matches any trusted pattern."""
    for regex in TRUSTED_HOSTS_RE:
        if regex.match(host):
            return True
    return False

def _is_public_ip(ip_str: str) -> bool:
    """Check if the IP is a public routable address."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return not (ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_multicast)
    except ValueError:
        # Not a valid IP address
        return False

def _resolve_host(host: str) -> bool:
    """Resolve the hostname and ensure at least one public IP is reachable."""
    try:
        # Resolve to all IPv4/IPv6 addresses
        infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return False

    for family, _, _, _, sockaddr in infos:
        ip_str = sockaddr[0]
        if _is_public_ip(ip_str):
            return True
    return False

# ----------------------------------------------------------------------
# Main validation function
# ----------------------------------------------------------------------
def validate_rss_link(rss_link: str) -> str:
    """
    Validate that the provided RSS feed URL points to a trusted provider
    and does not attempt SSRF.

    Parameters:
        rss_link (str): The URL to validate.

    Returns:
        str: A sanitized version of the original URL (scheme, netloc,
             path, params, query, fragment unchanged).

    Raises:
        ValueError: If the URL is malformed, uses an untrusted provider,
                    or resolves to a private/internal IP.
    """
    if not rss_link:
        raise ValueError("Empty RSS link provided")

    parsed = urlparse(rss_link)

    # Ensure scheme is http or https
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a hostname")

    # Check against trusted hosts
    if not _is_trusted_host(host):
        raise ValueError(f"Hostname '{host}' is not in the trusted providers list")

    # Resolve hostname and ensure at least one public IP
    if not _resolve_host(host):
        raise ValueError(f"Hostname '{host}' resolves to a private or non‑public IP")

    # Reconstruct the URL to normalise it (e.g., remove default ports)
    sanitized = urlunparse(parsed._replace(scheme=parsed.scheme.lower()))
    return sanitized

# ----------------------------------------------------------------------
# Example usage (uncomment for quick test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     try:
#         url = validate_rss_link("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
#         print(f"Validated URL: {url}")
#     except ValueError as e:
#         print(f"Validation failed: {e}")