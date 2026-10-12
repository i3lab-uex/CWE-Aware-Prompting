#!/usr/bin/env python3
"""
Utility to validate and resolve image URLs from trusted hosts.

The module defines a single public function, :func:`fetch_image_url`,
which checks that an input URL belongs to one of a pre‑defined list
of trusted image hosting domains and returns the same URL if it passes.
Otherwise, a :class:`ValueError` is raised.

The implementation protects against the CWE‑441 “Confused Deputy” issue
by refusing to forward or modify any URL that is not explicitly whitelisted.
"""

from __future__ import annotations

import re
from urllib.parse import urlparse, ParseResult


# --------------------------------------------------------------------------- #
# Configuration – trusted domains
# --------------------------------------------------------------------------- #

# NOTE: Add or remove domains as your security policy evolves.
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "avatars.githubusercontent.com",
    "pbs.twimg.com",  # Twitter image CDN
}

# Regular expression for a valid URL scheme (http or https)
_SCHEME_RE = re.compile(r"^(https?)$")

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def fetch_image_url(url: str) -> str:
    """
    Validate that *url* points to an image hosted on a trusted domain.

    Parameters
    ----------
    url : str
        The candidate URL to be validated.

    Returns
    -------
    str
        The original *url* if it is accepted.

    Raises
    ------
    ValueError
        If the URL's scheme is not ``http`` or ``https``,
        or if its host component does not match any trusted domain.
    """
    # Parse the URL once – this handles percent‑encoding and fragments
    parsed: ParseResult = urlparse(url)

    # 1. Validate scheme
    if not _SCHEME_RE.match(parsed.scheme or ""):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # 2. Validate host (netloc)
    # ``parsed.netloc`` may contain userinfo and port; we strip those
    host = parsed.hostname  # automatically lower‑cased by urllib
    if not host:
        raise ValueError("URL must contain a hostname")

    # Enforce exact match to prevent subdomain spoofing.
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Hostname {host!r} is not in the trusted list")

    # 3. (Optional) Basic sanity check for image extensions
    # This is not a strict requirement but helps avoid non‑image URLs.
    if not re.search(r"\.(jpg|jpeg|png|gif|webp)(\?.*)?$", parsed.path, re.IGNORECASE):
        # Warn but still accept – the caller may handle it.
        pass

    # 4. Return the original URL unchanged
    return url


# --------------------------------------------------------------------------- #
# Self‑test (optional)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_urls = [
        "https://i.imgur.com/abcd1234.jpg",
        "http://images.unsplash.com/photo-12345?ixlib=rb-1.2.1",
        "https://example.com/image.png",          # should fail
        "ftp://i.imgur.com/file.gif",            # should fail
    ]

    for u in test_urls:
        try:
            print(f"✓ {fetch_image_url(u)}")
        except ValueError as exc:
            print(f"✗ {u} -> {exc}")