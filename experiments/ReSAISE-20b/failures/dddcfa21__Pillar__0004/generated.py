#!/usr/bin/env python3
"""
Utility to validate and resolve image URLs from a set of trusted providers.
"""

from urllib.parse import urlparse, urlunparse
import re

# --------------------------------------------------------------------------- #
# Trusted image hosting providers – update as needed.
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "picsum.photos",
    "cdn.pixabay.com",
    "res.cloudinary.com",
}

# Allowed URL schemes.
ALLOWED_SCHEMES = {"http", "https"}


def _extract_domain(host: str) -> str:
    """
    Normalise a host by removing port information if present.
    """
    return host.split(":")[0].lower()


def check_image_url(img_address: str) -> str:
    """
    Validate that an image URL belongs to a trusted domain and uses a supported
    scheme.  The function returns the fully qualified URL if it passes all checks.

    Parameters
    ----------
    img_address : str
        The image URL to validate.

    Returns
    -------
    str
        The resolved, validated URL.

    Raises
    ------
    ValueError
        If the scheme is not http/https or if the domain is not in the trusted list.
    """
    if not isinstance(img_address, str):
        raise ValueError("img_address must be a string")

    # Parse the URL
    parsed = urlparse(img_address)

    # Scheme validation
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Domain validation
    domain = _extract_domain(parsed.netloc)
    if domain not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted image host: {domain}")

    # Rebuild the URL to ensure consistent formatting
    cleaned = parsed._replace(netloc=domain)
    return urlunparse(cleaned)


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Simple manual tests
    test_urls = [
        "https://i.imgur.com/abcd1234.jpg",
        "http://images.unsplash.com/photo-1587614313825-6c2b9e0d4a3f",
        "https://example.com/image.png",          # should fail
        "ftp://i.imgur.com/abcd1234.jpg",        # should fail
    ]

    for url in test_urls:
        try:
            print(f"✓ {check_image_url(url)}")
        except ValueError as e:
            print(f"✗ {url} -> {e}")