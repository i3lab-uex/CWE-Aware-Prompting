#!/usr/bin/env python3
"""
validate_image_url.py

Provides a single helper function `validate_image_url` that checks whether a supplied
image URL points to one of a pre‑defined set of trusted image hosting domains.
If the URL is valid, it is returned unchanged. Otherwise a ValueError is raised.

The implementation focuses on preventing SSRF attacks by strictly limiting
acceptable hostnames and schemes.
"""

from __future__ import annotations

import re
from urllib.parse import urlparse, urlunparse


# --------------------------------------------------------------------------- #
# Trusted domain configuration
# --------------------------------------------------------------------------- #

# A set of fully qualified hostnames that are considered safe.
# Add or remove entries as needed for your deployment environment.
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trustedsite.org",
    "storage.securehost.net",
}

# Allowed URL schemes.  Anything else will be rejected.
ALLOWED_SCHEMES = {"http", "https"}

# Regular expression to validate that a domain consists of allowed characters.
DOMAIN_REGEX = re.compile(r"^[a-zA-Z0-9.-]+$")


# --------------------------------------------------------------------------- #
# Core validation logic
# --------------------------------------------------------------------------- #

def validate_image_url(img_url: str) -> str:
    """
    Validate that *img_url* points to a trusted image host.

    Parameters
    ----------
    img_url : str
        The input URL to validate.

    Returns
    -------
    str
        The original URL if it is considered safe and well‑formed.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        or resolves to a domain not in ``TRUSTED_DOMAINS``.
    """
    if not isinstance(img_url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(img_url)

    # Scheme check (http/https only)
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Hostname presence
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid host")

    # Ensure the domain consists of allowed characters
    if not DOMAIN_REGEX.match(hostname):
        raise ValueError(f"Invalid domain name: {hostname!r}")

    # Normalize the hostname to lowercase for comparison
    normalized_host = hostname.lower()

    # Verify that the domain is in our trusted list
    if normalized_host not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {normalized_host!r}")

    # Re‑build the URL to ensure a consistent representation
    cleaned = urlunparse(
        (
            parsed.scheme.lower(),
            normalized_host,
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            parsed.fragment or "",
        )
    )

    return cleaned


# --------------------------------------------------------------------------- #
# Example usage (uncomment for testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_urls = [
        "https://images.example.com/photo.jpg",
        "http://cdn.trustedsite.org/avatars/user.png",
        "https://malicious.com/evil.jpg",
        "ftp://images.example.com/file.txt",
    ]

    for url in test_urls:
        try:
            print(f"Valid: {validate_image_url(url)}")
        except ValueError as exc:
            print(f"Invalid: {url} -> {exc}")