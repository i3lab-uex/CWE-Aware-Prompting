#!/usr/bin/env python3
"""
Utility to resolve an image URL only if it belongs to a trusted hosting domain.
"""

from __future__ import annotations

import re
import sys
from urllib.parse import urlparse, urlunparse


# List of trusted image hosting domains.
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trustedimage.org",
    "static.safe-site.net",
}

# Regular expression to detect IP addresses in URLs.
_IP_REGEX = re.compile(
    r"""
    ^
    (?:                       # IPv4
        (?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})
    |
        # IPv6
        \[
            (?:
                [0-9a-fA-F]{1,4}
                (?:\:[0-9a-fA-F]{1,4}){7}
            |
                (?:[0-9a-fA-F]{1,4}\:){1,7}:
            |
                (?:[0-9a-fA-F]{1,4}\:){1,6}:[0-9a-fA-F]{1,4}
            |
                (?:[0-9a-fA-F]{1,4}\:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}
            |
                (?:[0-9a-fA-F]{1,4}\:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}
            |
                (?:[0-9a-fA-F]{1,4}\:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}
            |
                (?:[0-9a-fA-F]{1,4}\:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}
            |
                [0-9a-fA-F]{1,4}\:(?::[0-9a-fA-F]{1,4}){1,6}
            |
                \:(?::[0-9a-fA-F]{1,4}){1,7}
            |
                ::(?::[0-9a-fA-F]{1,4}){0,6}
            )
        \]
    )
    $
    """,
    re.VERBOSE,
)


def _is_ip_address(host: str) -> bool:
    """Return True if the host is an IP address (IPv4 or IPv6)."""
    return bool(_IP_REGEX.match(host))


def resolve_image_url(image_url: str) -> str:
    """
    Resolve an image URL after verifying that it belongs to a trusted domain.

    Parameters
    ----------
    image_url : str
        The image URL to be resolved.

    Returns
    -------
    str
        The original URL if it is trusted and well‑formed.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        or its domain is not in the trusted list.
    """
    # Parse URL
    parsed = urlparse(image_url)

    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported or missing scheme: {parsed.scheme!r}")

    if not parsed.netloc:
        raise ValueError("URL must contain a host component")

    # Reject IP addresses to avoid accidental leaks
    if _is_ip_address(parsed.hostname):
        raise ValueError("IP addresses are not allowed as hosts")

    # Normalize host to lowercase for comparison
    hostname = parsed.hostname.lower()

    if hostname not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain {hostname!r} is not trusted")

    # Rebuild the URL to ensure canonical form (remove default ports)
    netloc = hostname
    if parsed.port:
        # Only keep port if it is non‑standard for the scheme
        default_port = 443 if parsed.scheme == "https" else 80
        if parsed.port != default_port:
            netloc = f"{hostname}:{parsed.port}"
    cleaned = urlunparse(
        (
            parsed.scheme,
            netloc,
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            parsed.fragment or "",
        )
    )

    return cleaned


# --------------------------------------------------------------------------- #
# Example usage (only executed when running this script directly)
if __name__ == "__main__":
    test_urls = [
        "https://images.example.com/path/to/image.png",
        "http://cdn.trustedimage.org/another-image.jpg",
        "https://untrusted.com/img.png",
        "http://127.0.0.1/image.jpg",
    ]

    for url in test_urls:
        try:
            resolved = resolve_image_url(url)
            print(f"✅ {url} -> {resolved}")
        except ValueError as exc:
            print(f"❌ {url} : {exc}", file=sys.stderr)