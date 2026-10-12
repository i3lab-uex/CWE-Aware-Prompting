#!/usr/bin/env python3
"""
Utility to validate image URLs against a whitelist of trusted providers.
"""

from urllib.parse import urlparse, urlunparse
from typing import List

# --------------------------------------------------------------------------- #
# Trusted image hosting providers (exact domain match or sub‑domains)
TRUSTED_DOMAINS: List[str] = [
    "images.unsplash.com",
    "cdn.pixabay.com",
    "i.imgur.com",
    "storage.googleapis.com",  # e.g. Google Cloud Storage buckets
    "images.weserv.nl",
]

# Supported URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def _is_trusted_domain(netloc: str) -> bool:
    """
    Check if the netloc (host part of a URL) belongs to one of the trusted domains.
    Sub‑domains are accepted (e.g., foo.images.unsplash.com).
    """
    # Remove port if present
    host = netloc.split(":")[0].lower()
    for domain in TRUSTED_DOMAINS:
        if host == domain or host.endswith("." + domain):
            return True
    return False


def check_image_url(img_address: str) -> str:
    """
    Validate an image URL.

    Parameters
    ----------
    img_address : str
        The candidate image URL.

    Returns
    -------
    str
        The fully resolved, validated URL (unchanged if already absolute).

    Raises
    ------
    ValueError
        If the URL scheme is unsupported or its domain is not trusted.
    """
    if not isinstance(img_address, str):
        raise ValueError("img_address must be a string")

    parsed = urlparse(img_address)

    # Validate scheme
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Validate domain
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not trusted")

    # Reconstruct the URL to ensure consistency (e.g., no duplicate slashes)
    cleaned = urlunparse(parsed._replace(scheme=parsed.scheme.lower()))
    return cleaned