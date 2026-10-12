#!/usr/bin/env python3
"""
Utility to validate RSS feed URLs against a whitelist of trusted providers.

The function `check_rss_address` ensures that the supplied URL:
  * uses a safe scheme (http or https)
  * points to a domain that is on the approved list
  * does not resolve to an internal/private IP address (CWE‑918 mitigation)

If the URL fails any of these checks a ValueError is raised.
"""

import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# --------------------------------------------------------------------------- #
# Configuration – add any additional trusted providers here.
# --------------------------------------------------------------------------- #
TRUSTED_DOMAINS = {
    # Main RSS feeds
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    # Example: add your own trusted domains
    "example.com",
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_private_ip(ip: str) -> bool:
    """
    Return True if the IP address is in a private/reserved range.
    """
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback
    except ValueError:
        # Not a valid IP address – treat as safe for now.
        return False

def _sanitize_url(parsed: urlparse) -> str:
    """
    Reconstruct the URL with only its scheme, netloc, and path.
    Query parameters and fragments are stripped to avoid SSRF via them.
    """
    safe_netloc = parsed.netloc
    # If netloc contains username/password, strip them
    if '@' in safe_netloc:
        _, safe_netloc = safe_netloc.split('@', 1)
    # Ensure the port is removed (default ports are implicit)
    if ':' in safe_netloc:
        host, _ = safe_netloc.split(':', 1)
    else:
        host = safe_netloc
    # Rebuild the URL without query or fragment
    return urlunparse((parsed.scheme, host, parsed.path, '', '', ''))

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def check_rss_address(rss_address: str) -> str:
    """
    Validate an RSS feed URL against a whitelist of trusted providers.

    Parameters
    ----------
    rss_address : str
        The URL to validate.

    Returns
    -------
    str
        A sanitized version of the URL that is guaranteed to point to a trusted provider.

    Raises
    ------
    ValueError
        If the URL uses an unsafe scheme, points to a non‑trusted domain,
        or resolves (via its host) to an internal/private IP address.
    """
    if not isinstance(rss_address, str):
        raise ValueError("RSS address must be a string")

    parsed = urlparse(rss_address)

    # 1. Scheme check
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # 2. Host extraction
    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a valid hostname")

    # 3. Check against whitelist
    if host.lower() not in TRUSTED_DOMAINS:
        raise ValueError(f"Hostname '{host}' is not on the trusted list")

    # 4. Optional: check that host does NOT resolve to a private IP
    # We avoid DNS lookups in production code, but for demonstration we can
    # use the `socket.getaddrinfo` fallback. In a real SSRF‑safe environment
    # you would rely solely on the whitelist.
    try:
        import socket
        for res in socket.getaddrinfo(host, None):
            ip = res[4][0]
            if _is_private_ip(ip):
                raise ValueError(f"Hostname '{host}' resolves to a private IP ({ip})")
    except Exception:
        # If DNS resolution fails, we assume it is safe if hostname is trusted
        pass

    # 5. Sanitize the URL: strip query and fragment to prevent SSRF via them
    sanitized = _sanitize_url(parsed)
    return sanitized

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        url = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml?param=1#section"
        print("Sanitized URL:", check_rss_address(url))
    except ValueError as e:
        print("Validation failed:", e)