#!/usr/bin/env python3
"""
Utility to validate image URLs against a whitelist of trusted domains.
"""

from urllib.parse import urlparse
from typing import List

# --------------------------------------------------------------------------- #
# Configuration: list of fully qualified domains that are allowed.
# Add or remove entries as your policy changes.
TRUSTED_DOMAINS: List[str] = [
    "imgur.com",
    "i.imgur.com",
    "pbs.twimg.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    # Add more trusted image hosts here
]

# --------------------------------------------------------------------------- #
def _is_trusted_domain(netloc: str) -> bool:
    """
    Check whether the given netloc (hostname + optional port) is part of
    TRUSTED_DOMAINS. Subdomains are considered valid only if they match a
    domain exactly or end with '.' + domain.

    Parameters
    ----------
    netloc : str
        The network location part of a parsed URL.

    Returns
    -------
    bool
        True if the domain is trusted, False otherwise.
    """
    # Strip optional port number for comparison
    host = netloc.split(":")[0].lower()

    for domain in TRUSTED_DOMAINS:
        # Exact match
        if host == domain.lower():
            return True
        # Subdomain check: host must end with '.' + domain
        if host.endswith("." + domain.lower()):
            return True
    return False


def fetch_image_url(url: str) -> str:
    """
    Resolve an image URL and verify that its domain is trusted.

    Parameters
    ----------
    url : str
        The original URL to validate.

    Returns
    -------
    str
        The same URL if it passes validation.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme or its domain is not trusted.
    """
    if not isinstance(url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(url)

    # Only allow HTTP and HTTPS schemes
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure the netloc (host) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (host)")

    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.netloc}")

    # All checks passed; return the original URL unchanged
    return url


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Simple manual tests
    test_urls = [
        "https://i.imgur.com/abcd1234.png",
        "http://pbs.twimg.com/media/XYZ.jpg",
        "https://example.com/image.png",          # should fail
        "ftp://imgur.com/file.jpg",               # unsupported scheme
    ]

    for test in test_urls:
        try:
            print(f"✔ {fetch_image_url(test)}")
        except ValueError as exc:
            print(f"✘ {test} -> {exc}")