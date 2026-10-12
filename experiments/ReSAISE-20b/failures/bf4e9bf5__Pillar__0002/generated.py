#!/usr/bin/env python3
"""
Utility for resolving image URLs only if they belong to a trusted host.

The function `resolve_image_url` parses the supplied URL, validates that
its scheme is HTTP or HTTPS, and checks the host against a whitelist of
trusted image‑hosting domains.  If the URL is not from an approved host,
`ValueError` is raised.

Security notes:
- The function does *not* perform a DNS lookup; it relies solely on
  the hostname in the URL.  This avoids potential DNS rebinding attacks.
- Only HTTP(S) schemes are allowed to prevent protocols such as `file://`
  from being inadvertently used.
"""

from __future__ import annotations

import urllib.parse
from typing import List, Tuple


# --------------------------------------------------------------------------- #
# Trusted domains list.  Extend this list with any additional hosts that are
# considered safe for serving images.
# --------------------------------------------------------------------------- #
TRUSTED_DOMAINS: List[str] = [
    "images.example.com",
    "cdn.trustedsite.org",
    "static.safe-host.net",
]


def _normalize_host(host: str) -> str:
    """
    Normalise the host component to a canonical form.

    This removes any trailing dot and converts the hostname to lower case,
    ensuring consistent comparison with the trusted list.

    Parameters
    ----------
    host : str
        The hostname extracted from a parsed URL.

    Returns
    -------
    str
        Normalised hostname.
    """
    return host.rstrip(".").lower()


def resolve_image_url(image_url: str) -> str:
    """
    Resolve an image URL after verifying that it belongs to a trusted host.

    Parameters
    ----------
    image_url : str
        The URL string pointing to an image resource.

    Returns
    -------
    str
        The same URL if it is safe; otherwise, a ValueError is raised.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP(S) or if the host is not in the trusted list.
    """
    # Parse the URL
    parsed = urllib.parse.urlparse(image_url)

    # Validate scheme: only http and https are allowed
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Normalise and validate host
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    host = _normalize_host(parsed.hostname)

    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted image host: {host!r}")

    # Reconstruct the URL to ensure consistent formatting
    cleaned = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return cleaned


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_urls = [
        "https://images.example.com/path/to/image.png",
        "http://cdn.trustedsite.org/img.jpg?size=large",
        "https://malicious.com/evil.png",
    ]

    for url in test_urls:
        try:
            resolved = resolve_image_url(url)
            print(f"✅ {resolved}")
        except ValueError as exc:
            print(f"❌ {url} -> {exc}")