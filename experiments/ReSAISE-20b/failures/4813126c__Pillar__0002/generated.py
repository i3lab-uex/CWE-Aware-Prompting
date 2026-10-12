#!/usr/bin/env python3
"""
Utility to verify that an image URL points to a trusted hosting domain.
"""

from urllib.parse import urlparse
from typing import Set


# Trusted domains (add or remove as required)
_TRUSTED_DOMAINS: Set[str] = {
    "images.example.com",
    "cdn.imghost.com",
    "static.myapp.net",
}

# Accepted URL schemes
_ACCEPTED_SCHEMES = {"http", "https"}


def verify_image_url(img_url: str) -> str:
    """
    Validate that the supplied image URL uses an approved scheme and domain.

    Parameters
    ----------
    img_url : str
        The URL of the image to verify.

    Returns
    -------
    str
        The original URL if it is considered safe and trusted.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https or if its domain does not match any of the
        trusted domains.
    """
    if not isinstance(img_url, str):
        raise ValueError("Image URL must be a string")

    parsed = urlparse(img_url)

    # Scheme validation
    if parsed.scheme.lower() not in _ACCEPTED_SCHEMES:
        raise ValueError(f"Unrecognized URL scheme '{parsed.scheme}'. Only http/https are allowed.")

    # Domain validation
    netloc = parsed.netloc.lower()
    if not any(netloc == domain or netloc.endswith("." + domain) for domain in _TRUSTED_DOMAINS):
        raise ValueError(f"Domain '{netloc}' is not in the list of trusted image hosts.")

    # All checks passed; return the original URL
    return img_url