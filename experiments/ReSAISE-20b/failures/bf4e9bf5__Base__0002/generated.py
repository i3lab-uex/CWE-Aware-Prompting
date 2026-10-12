#!/usr/bin/env python3
"""
Utility to resolve image URLs while guarding against SSRF.

The function checks that the host of a supplied URL is in a predefined
list of trusted image hosting domains.  If the domain is not trusted,
a ValueError is raised.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import re
from urllib.parse import urlparse, ParseResult
from typing import List, Set


# --------------------------------------------------------------------------- #
# Trusted domains – extend this list with any additional hosts you consider safe
# --------------------------------------------------------------------------- #
_TRUSTED_DOMAINS: Set[str] = {
    "imgur.com",
    "i.imgur.com",
    "unsplash.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "flickr.com",
    "static.flickr.com",
    "picsum.photos",
}

# Regular expression to detect IP addresses in the host part
_IP_REGEX = re.compile(
    r"""
    ^
    (?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
        |
        # IPv6
        \[
            (?:
                [0-9a-fA-F]{1,4}
                (?:\:[0-9a-fA-F]{1,4}){7}
            |
                ::[0-9a-fA-F]{1,4}(?::[0-9a-fA-F]{1,4}){0,6}
            |
                [0-9a-fA-F]{1,4}::[0-9a-fA-F]{1,4}(?::[0-9a-fA-F]{1,4}){0,5}
            |
                [0-9a-fA-F]{1,4}(?::[0-9a-fA-F]{1,4}){2,7}::
            |
                ::[0-9a-fA-F]{1,4}(?::[0-9a-fA-F]{1,4}){0,5}:
            |
                [0-9a-fA-F]{1,4}(?::[0-9a-fA-F]{1,4}){3,7}
            |
                [0-9a-fA-F]{1,4}(?::[0-9a-fA-F]{1,4}){3,7}:
            )
        \]
    )
    $
    """,
    re.VERBOSE,
)


def _is_ip_address(host: str) -> bool:
    """
    Return True if the host string is an IP address (IPv4 or IPv6).
    """
    return bool(_IP_REGEX.match(host))


def _normalize_domain(domain: str) -> str:
    """
    Normalize domain names by stripping any trailing dot and converting to lowercase.
    """
    return domain.rstrip(".").lower()


def resolve_image_url(image_url: str) -> str:
    """
    Resolve an image URL only if it belongs to a trusted domain.

    Parameters
    ----------
    image_url : str
        The URL of the image to be validated.

    Returns
    -------
    str
        The original URL if it is from a trusted domain.

    Raises
    ------
    ValueError
        If the URL's host is not in the trusted list or if it resolves to an IP address.
    """
    # Parse URL
    parsed: ParseResult = urlparse(image_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL: missing scheme or host")

    # Reject URLs that use a non-HTTP(S) scheme
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'")

    host = _normalize_domain(parsed.hostname or "")

    # Reject URLs that point to IP addresses
    if not host:
        raise ValueError("URL does not contain a valid hostname")

    if _is_ip_address(host):
        raise ValueError("URL host is an IP address, which is not trusted")

    # Check if the host or any of its parent domains are in the trusted list
    domain_parts = host.split(".")
    for i in range(len(domain_parts)):
        candidate = ".".join(domain_parts[i:])
        if candidate in _TRUSTED_DOMAINS:
            # URL is from a trusted domain
            return image_url

    raise ValueError(f"Domain '{host}' is not in the list of trusted image hosts")


# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_urls = [
        "https://i.imgur.com/example.png",
        "http://cdn.pixabay.com/photo/2020/01/01/12/34/example.jpg",
        "https://malicious.com/bad.png",
        "http://127.0.0.1/image.jpg",
    ]

    for url in test_urls:
        try:
            resolved = resolve_image_url(url)
            print(f"✅ {url} -> {resolved}")
        except ValueError as exc:
            print(f"❌ {url} : {exc}")