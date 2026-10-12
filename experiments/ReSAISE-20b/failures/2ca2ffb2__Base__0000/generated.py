#!/usr/bin/env python3
"""
Utility to safely resolve an image URL against a whitelist of trusted
image‑hosting domains.  It mitigates SSRF (CWE‑918) by rejecting any
URL that does not point to a known, safe domain and by enforcing the
use of HTTP(S) only.
"""

from __future__ import annotations

import ipaddress
import re
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------------- #
# Trusted domain configuration
# --------------------------------------------------------------------------- #

# A set of domains that are considered safe for image hosting.
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "static.example.com",  # example placeholder
}

# Allow subdomains of the trusted domains (e.g. cdn.example.com)
ALLOW_SUBDOMAINS = True

# Regular expression for validating hostnames (RFC 1035)
HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}$"
)


def _is_ip_address(host: str) -> bool:
    """
    Return True if the host is a valid IPv4 or IPv6 address.
    """
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def _is_trusted_domain(host: str) -> bool:
    """
    Determine if a hostname is within the TRUSTED_DOMAINS set.
    Handles subdomains when ALLOW_SUBDOMAINS is True.
    """
    # Reject IP addresses outright
    if _is_ip_address(host):
        return False

    # Validate hostname syntax
    if not HOSTNAME_RE.match(host):
        return False

    host = host.lower()
    if host in TRUSTED_DOMAINS:
        return True

    if ALLOW_SUBDOMAINS:
        # Check if the host ends with any trusted domain
        for td in TRUSTED_DOMAINS:
            if host.endswith("." + td):
                return True

    return False


def fetch_image_url(url: str) -> str:
    """
    Resolve an image URL, ensuring it points to a trusted domain.

    Parameters
    ----------
    url : str
        The original image URL provided by an external source.

    Returns
    -------
    str
        The normalized, verified image URL.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP(S) or if the domain is untrusted.
    """
    # Parse the URL
    parsed = urlparse(url)

    # Scheme validation
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unrecognized URL scheme: {parsed.scheme}")

    # Domain validation
    if not parsed.hostname or not _is_trusted_domain(parsed.hostname):
        raise ValueError(f"Domain '{parsed.hostname}' is not trusted")

    # Rebuild the URL to ensure consistent formatting
    safe_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return safe_url


# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_urls = [
        "https://i.imgur.com/abcd1234.png",
        "http://images.unsplash.com/photo-12345.jpg?foo=bar",
        "https://evil.com/hack.png",
        "ftp://i.imgur.com/file.jpg",
        "http://127.0.0.1/secret.png",
    ]

    for u in test_urls:
        try:
            print(f"Verified: {fetch_image_url(u)}")
        except ValueError as exc:
            print(f"Rejected: {u} -> {exc}")