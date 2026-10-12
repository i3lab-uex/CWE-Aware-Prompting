#!/usr/bin/env python3
"""
Utility to validate and sanitize RSS feed URLs before use.
This protects against SSRF (CWE‑918) by ensuring the URL points only to
trusted external providers and does not resolve to any internal network
addresses.
"""

from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse, urlunparse, ParseResult

# --------------------------------------------------------------------------- #
# Trusted RSS providers
# --------------------------------------------------------------------------- #
_TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",          # google news RSS
    "rss.cnn.com",
    "feeds.reuters.com",
    "feedproxy.google.com",     # feed proxy
    "rss.feedsportal.com",
    # Add more domains as needed
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _is_internal_ip(ip: str) -> bool:
    """
    Return True if the IP address is in a private, loopback,
    link-local, or reserved range.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return (
            addr.is_private
            or addr.is_loopback
            or addr.is_link_local
            or addr.is_reserved
        )
    except ValueError:
        # Invalid IP address; treat as non‑internal
        return False


def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve the hostname to all IP addresses it maps to.
    Raises socket.gaierror if resolution fails.
    """
    return list(set(socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)))


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def clean_feed_link(rss_link: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_link : str
        The raw RSS feed URL provided by the user or another component.

    Returns
    -------
    str
        A sanitized, validated URL that points to a trusted provider.

    Raises
    ------
    ValueError
        If the URL is malformed, not HTTPS/HTTP, resolves to an internal IP,
        or does not belong to a trusted domain.
    """
    if not isinstance(rss_link, str):
        raise ValueError("RSS link must be a string")

    parsed: ParseResult = urlparse(rss_link)

    # 1. Basic scheme validation
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # 2. Netloc (hostname) must be present
    if not parsed.hostname:
        raise ValueError("URL does not contain a valid hostname")

    # 3. Domain must be in the trusted list (case‑insensitive)
    hostname = parsed.hostname.lower()
    if hostname not in _TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {hostname}")

    # 4. Resolve hostname to IP(s) and ensure none are internal
    try:
        addrinfo = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Failed to resolve hostname {hostname}: {exc}") from exc

    for family, _, _, _, sockaddr in addrinfo:
        ip = sockaddr[0]
        if _is_internal_ip(ip):
            raise ValueError(
                f"Hostname {hostname} resolves to internal IP {ip}, "
                "which is not allowed."
            )

    # 5. Re‑assemble the URL to ensure no path traversal or
    #    query parameters that could alter behavior.
    sanitized = ParseResult(
        scheme=parsed.scheme,
        netloc=f"{hostname}{':' + str(parsed.port) if parsed.port else ''}",
        path=parsed.path or "/",
        params="",
        query="",
        fragment="",
    )
    return urlunparse(sanitized)


# --------------------------------------------------------------------------- #
# Example usage (remove or guard with __name__ == "__main__" in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_urls = [
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "http://feeds.bbci.co.uk/news/rss.xml",
        "https://example.com/feed",                     # untrusted
        "http://localhost/rss.xml",                    # internal
    ]

    for url in test_urls:
        try:
            print(f"Validating: {url}")
            print("  =>", clean_feed_link(url))
        except ValueError as e:
            print(f"  ! Error: {e}")