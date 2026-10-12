#!/usr/bin/env python3
"""
Utility to validate an image URL against a list of trusted host domains.

The function `check_image_url` ensures that the supplied URL:
1. Uses a supported scheme (`http` or `https`).
2. Resolves to one of the trusted domains.
3. Does not point to an IP address, localhost or other disallowed hostnames.

If the URL fails any check a `ValueError` is raised.
"""

from __future__ import annotations

import ipaddress
import re
from urllib.parse import urlparse, ParseResult

# --------------------------------------------------------------------------- #
# Trusted image hosting providers
# --------------------------------------------------------------------------- #
TRUSTED_DOMAINS = {
    # Generic CDN / image hosting services
    "images.unsplash.com",
    "cdn.pixabay.com",
    # Flickr and similar
    "i.imgur.com",
    "farm1.staticflickr.com",
    # Cloud storage providers (public buckets)
    "storage.googleapis.com",
    "s3.amazonaws.com",
    # Self-hosted or CDN domains
    "cdn.example.org",
}

# Regular expression to detect IPv4 or IPv6 addresses in a hostname
IP_REGEX = re.compile(r"""
    ^(?:
        # IPv4: 0-255.0-255.0-255.0-255
        (?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})
        |
        # IPv6: [hex digits separated by colons]
        \[
            (?:
                ([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}
                |
                ([0-9a-fA-F]{1,4}:){1,7}:
                |
                ([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}
                |
                ([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}
                |
                ([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}
                |
                ([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}
                |
                ([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}
                |
                [0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})
                |
                :((:[0-9a-fA-F]{1,4}){1,7}|:)
            )
        \]
    )$
""", re.VERBOSE)

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _is_ip_address(host: str) -> bool:
    """Return True if the host is a valid IP address (IPv4 or IPv6)."""
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def _is_localhost(host: str) -> bool:
    """Return True if the host resolves to localhost."""
    # Common representations of localhost
    return host in {"localhost", "127.0.0.1", "::1"}


def _is_trusted_domain(host: str) -> bool:
    """Check if host matches any trusted domain (exact or subdomain)."""
    # Normalize to lowercase
    host = host.lower()
    for domain in TRUSTED_DOMAINS:
        if host == domain or host.endswith("." + domain):
            return True
    return False


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def check_image_url(img_address: str) -> str:
    """
    Validate an image URL against a whitelist of trusted domains.

    Parameters
    ----------
    img_address : str
        The input image URL to validate.

    Returns
    -------
    str
        The original URL if it is considered safe and trusted.

    Raises
    ------
    ValueError
        If the URL scheme is unsupported, or if the host is not trusted,
        or if it resolves to an IP address or localhost.
    """
    # Parse the URL
    parsed: ParseResult = urlparse(img_address)

    # Ensure scheme is http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure netloc (host) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a host")

    # Extract hostname (without port)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject IP addresses and localhost
    if _is_ip_address(host):
        raise ValueError("IP address hosts are not allowed")
    if _is_localhost(host):
        raise ValueError("Localhost addresses are not allowed")

    # Verify the host is within the trusted list
    if not _is_trusted_domain(host):
        raise ValueError(f"Untrusted host domain: {host}")

    # Reconstruct the URL to ensure it is fully qualified
    safe_url = parsed.geturl()
    return safe_url


# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_urls = [
        "https://images.unsplash.com/photo-1234567890",
        "http://i.imgur.com/abcde.png",
        "https://example.com/image.jpg",  # untrusted
    ]

    for url in test_urls:
        try:
            print(f"Valid: {check_image_url(url)}")
        except ValueError as e:
            print(f"Invalid: {url} -> {e}")