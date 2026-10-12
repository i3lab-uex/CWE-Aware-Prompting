#!/usr/bin/env python3
"""
Utility to validate an image URL against a whitelist of trusted hosting domains.
"""

from __future__ import annotations

import re
from urllib.parse import urlparse, urlunparse, ParseResult


# --------------------------------------------------------------------------- #
# Trusted domain list (add/remove as needed)
# --------------------------------------------------------------------------- #
TRUSTED_DOMAINS = {
    "imgur.com",
    "images.unsplash.com",
    "picsum.photos",
    "cdn.pixabay.com",
    "flickr.com",
}

# --------------------------------------------------------------------------- #
# Regular expression to validate hostnames (basic RFC 1035 compliance)
# --------------------------------------------------------------------------- #
HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}$"
)


def _is_valid_hostname(hostname: str) -> bool:
    """
    Basic validation of a hostname.
    Returns True if the hostname matches RFC 1035 rules.
    """
    return bool(HOSTNAME_RE.match(hostname))


def _canonicalize_domain(domain: str) -> str:
    """
    Lowercase the domain for comparison. Trailing dots are removed.
    """
    return domain.rstrip(".").lower()


def check_image_url(img_address: str) -> str:
    """
    Validate an image URL and return the canonical absolute URL if it is
    hosted on a trusted provider.

    Parameters
    ----------
    img_address : str
        The input image URL (may be absolute or relative).

    Returns
    -------
    str
        The fully resolved, canonical URL.

    Raises
    ------
    ValueError
        If the scheme is unsupported, the domain is not trusted,
        or the URL is malformed.
    """
    if not isinstance(img_address, str):
        raise ValueError("img_address must be a string")

    # Parse the URL
    parsed = urlparse(img_address)

    # Reject unsupported schemes or missing scheme
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Ensure the netloc (host) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a host component")

    # Validate the hostname
    if not _is_valid_hostname(parsed.hostname):
        raise ValueError(f"Invalid hostname: {parsed.hostname!r}")

    # Check that the host is in the trusted list
    canonical_host = _canonicalize_domain(parsed.hostname)
    if canonical_host not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain {canonical_host!r} is not trusted")

    # Reconstruct the URL to ensure a clean representation
    cleaned = ParseResult(
        scheme=parsed.scheme,
        netloc=canonical_host,
        path=parsed.path or "",
        params="",
        query=parsed.query,
        fragment="",
    )
    return urlunparse(cleaned)


# --------------------------------------------------------------------------- #
# Example usage (for testing only; remove or guard under `if __name__ == "__main__":`)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_urls = [
        "https://i.imgur.com/abc123.jpg",
        "http://images.unsplash.com/photo-1234567890?auto=format&fit=crop",
        "https://evil.com/malicious.png",
    ]

    for url in test_urls:
        try:
            print(f"Valid: {check_image_url(url)}")
        except ValueError as exc:
            print(f"Invalid: {url} -> {exc}")