#!/usr/bin/env python3
"""
validate_image_url

This module provides a single function `validate_image_url` that checks whether
a supplied image URL belongs to a list of trusted image hosting providers.
If the URL is valid, the function returns the fully resolved (normalized)
URL. Otherwise a ValueError is raised.

The implementation uses only standard library modules to avoid external
dependencies and follows best practices for URL parsing and validation.
"""

from __future__ import annotations

import urllib.parse
from typing import Final, Set


# --------------------------------------------------------------------------- #
# Trusted domains (add or remove providers as needed)
# --------------------------------------------------------------------------- #
_TRUSTED_DOMAINS: Final[Set[str]] = {
    "imgur.com",
    "i.imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "picsum.photos",
    "flickr.com",
    "cdn.pexels.com",
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _is_trusted_domain(netloc: str) -> bool:
    """
    Check whether the given netloc (domain + optional port) is a trusted domain
    or a sub‑domain of one.

    Parameters
    ----------
    netloc : str
        The network location part of a URL (e.g., "i.imgur.com:443").

    Returns
    -------
    bool
        True if the domain is trusted, False otherwise.
    """
    # Remove port number if present
    domain = netloc.split(":")[0].lower()

    # Exact match or sub‑domain
    for trusted in _TRUSTED_DOMAINS:
        if domain == trusted or domain.endswith("." + trusted):
            return True
    return False


def _normalize_url(parsed: urllib.parse.ParseResult) -> str:
    """
    Reconstruct a URL from its parsed components, ensuring consistent
    formatting (lowercase scheme and netloc).

    Parameters
    ----------
    parsed : urllib.parse.ParseResult

    Returns
    -------
    str
        The normalized URL string.
    """
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    path = urllib.parse.quote(parsed.path)
    params = urllib.parse.quote_plus(parsed.params) if parsed.params else ""
    query = urllib.parse.quote_plus(parsed.query, safe="=&") if parsed.query else ""
    fragment = urllib.parse.quote_plus(parsed.fragment) if parsed.fragment else ""

    return urllib.parse.urlunparse(
        (scheme, netloc, path, params, query, fragment)
    )


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def validate_image_url(img_url: str) -> str:
    """
    Validate that the supplied image URL points to a trusted domain and uses
    a supported scheme (http or https).

    Parameters
    ----------
    img_url : str
        The image URL to validate.

    Returns
    -------
    str
        The fully resolved and normalized URL if it is valid.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, or its domain is not trusted.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    parsed = urllib.parse.urlparse(img_url)

    # Scheme check
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Domain check
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain)")

    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not trusted")

    # Return normalized URL
    return _normalize_url(parsed)


# --------------------------------------------------------------------------- #
# Example usage (for manual testing)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_urls = [
        "https://i.imgur.com/abcd1234.jpg",
        "http://cdn.pixabay.com/photo/2021/04/12/15/22/beach-6198929_1280.jpg",
        "https://example.com/image.png",          # should fail
        "ftp://i.imgur.com/abcd1234.jpg",        # should fail
    ]

    for url in test_urls:
        try:
            print(f"Valid: {validate_image_url(url)}")
        except ValueError as exc:
            print(f"Invalid: {url} -> {exc}")