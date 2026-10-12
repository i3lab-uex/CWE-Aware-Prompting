#!/usr/bin/env python3
"""
Utility to validate image URLs against a whitelist of trusted domains.
"""

from urllib.parse import urlparse
import re

# --------------------------------------------------------------------------- #
# Configuration: list of trusted image‑hosting domains. Add or remove entries
# as needed. Each entry is a domain suffix; sub‑domains are accepted.
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "picsum.photos",
    # add more domains here
}

# --------------------------------------------------------------------------- #
def _is_trusted_domain(netloc: str) -> bool:
    """
    Determine whether a hostname/netloc belongs to one of the trusted domains.
    Handles optional port numbers and case insensitivity.

    Parameters
    ----------
    netloc : str
        The network location part of a parsed URL (e.g., 'example.com:80').

    Returns
    -------
    bool
        True if the host matches a trusted domain; False otherwise.
    """
    # Remove any port information
    host = netloc.split(":")[0].lower()

    # Direct match or sub‑domain match
    for domain in TRUSTED_DOMAINS:
        if host == domain or host.endswith("." + domain):
            return True
    return False

# --------------------------------------------------------------------------- #
def check_image_link(image_link: str) -> str:
    """
    Validate an image URL and return the same URL if it is considered safe.

    Parameters
    ----------
    image_link : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it passes validation checks.

    Raises
    ------
    ValueError
        If the URL has an unsupported scheme or does not belong to a trusted domain.
    """
    if not isinstance(image_link, str):
        raise ValueError("image_link must be a string")

    parsed = urlparse(image_link)

    # Scheme validation: only http and https are allowed
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure that the hostname is present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (hostname)")

    # Domain whitelist check
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.hostname}")

    # The URL is considered safe; return it unchanged
    return image_link

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Simple self‑test when executed directly
    test_urls = [
        "https://i.imgur.com/abc123.png",
        "http://cdn.pixabay.com/photo/2021/01/01/12/34/56/sample.jpg",
        "https://malicious.com/hack.png",
        "ftp://imgur.com/file.png",
    ]

    for url in test_urls:
        try:
            print(f"✅ {check_image_link(url)}")
        except ValueError as exc:
            print(f"❌ {url} → {exc}")