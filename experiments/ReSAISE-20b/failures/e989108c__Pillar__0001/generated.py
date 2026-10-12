#!/usr/bin/env python3
"""
Utility module for validating and normalizing image URLs.

The `get_image_link` function ensures that only URLs from a predefined
list of trusted image hosting providers are accepted. It validates the
scheme, domain, and optionally the file extension to mitigate potential
security risks such as accidental inclusion of non‑image content or
untrusted domains.
"""

from __future__ import annotations

import re
from urllib.parse import urlparse, unquote


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Allowed URL schemes.
ALLOWED_SCHEMES = {"http", "https"}

# Trusted domains and optional subdomain patterns.
# Each entry is a regex that matches the domain portion of the URL.
TRUSTED_DOMAIN_PATTERNS = [
    r"^imgur\.com$",
    r"^i\.imgur\.com$",
    r"^cdn\.pixabay\.com$",
    r"^images\.unsplash\.com$",
]

# Optional: Allowed image file extensions (case‑insensitive).
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

# Compile regexes for performance.
_compiled_domain_patterns = [re.compile(p, re.IGNORECASE) for p in TRUSTED_DOMAIN_PATTERNS]
_allowed_ext_pattern = re.compile(
    r"(?i)\.(?:jpg|jpeg|png|gif|webp)$"
)


# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def get_image_link(link_image: str) -> str:
    """
    Validate and resolve an image URL against a whitelist of trusted providers.

    Parameters
    ----------
    link_image : str
        The URL string to validate and normalize.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL has an unsupported scheme, untrusted domain,
        or does not point to a recognized image file type.
    """
    if not isinstance(link_image, str):
        raise ValueError("link_image must be a string")

    # Parse the URL
    parsed = urlparse(link_image)

    # 1. Validate scheme
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # 2. Validate domain against the whitelist
    netloc = parsed.netloc.lower()
    if not any(p.match(netloc) for p in _compiled_domain_patterns):
        raise ValueError(f"Untrusted domain: {netloc}")

    # 3. Optional: Ensure the path ends with a known image extension
    if not _allowed_ext_pattern.search(parsed.path):
        raise ValueError(f"URL does not point to a recognized image file: {parsed.path}")

    # 4. Return the original (or optionally, a normalized) URL
    # Normalization can include percent‑decoding the path and query.
    # Here we simply return the input unchanged to preserve any
    # intentional encoding (e.g., spaces as %20).
    return link_image


# --------------------------------------------------------------------------- #
# Example usage (uncomment for testing)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     test_urls = [
#         "https://i.imgur.com/abc123.jpg",
#         "http://cdn.pixabay.com/photo/2021/04/01/10/00/sample.png",
#         "https://example.com/image.gif",  # Should raise ValueError
#     ]
#
#     for url in test_urls:
#         try:
#             print(f"Validating: {url}")
#             result = get_image_link(url)
#             print(f" -> Validated URL: {result}\n")
#         except ValueError as e:
#             print(f" -> Validation failed: {e}\n")