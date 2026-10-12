#!/usr/bin/env python3
"""
Utility to validate that an image URL points to a trusted host.

The function checks:
* The scheme is either http or https.
* The hostname matches one of the approved image hosting domains.

If any check fails, a ValueError is raised.  The function returns the
original URL unchanged when all checks pass.

Security note: No network request is performed, so there is no risk of
remote code execution or resource exhaustion due to redirects.  The
function only parses the URL and compares against a static whitelist,
avoiding potential issues related to CWE‑664.
"""

from urllib.parse import urlparse
from typing import List

# --------------------------------------------------------------------------- #
# Trusted image hosting domains.  Add or remove hosts as your policy requires.
# The list is intentionally short; extend it responsibly.
TRUSTED_DOMAINS: List[str] = [
    "imgur.com",
    "i.imgur.com",
    "cdn.discordapp.com",
    "pbs.twimg.com",
    "i.redd.it",
    "flickr.com",
    "cdn.pixabay.com",
]

# --------------------------------------------------------------------------- #
def check_image_link(image_link: str) -> str:
    """
    Validate that an image URL belongs to a trusted domain.

    Parameters
    ----------
    image_link : str
        The URL of the image to verify.

    Returns
    -------
    str
        The original URL if it passes validation checks.

    Raises
    ------
    ValueError
        If the URL's scheme is not HTTP(S) or if its domain is not in the
        trusted list.
    """
    # Parse URL
    parsed = urlparse(image_link)

    # Validate scheme
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Extract hostname (case‑insensitive comparison)
    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a valid hostname")

    # Normalise to lowercase for comparison
    host = host.lower()

    # Check against trusted domains
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted image host: {host!r}")

    # All checks passed
    return image_link

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Simple test harness
    test_urls = [
        "https://i.imgur.com/example.png",
        "http://cdn.discordapp.com/attachments/12345/image.jpg",
        "https://malicious.example.com/hack.png",
        "ftp://i.imgur.com/file.jpg",
    ]

    for url in test_urls:
        try:
            verified = check_image_link(url)
            print(f"✅ Valid: {verified}")
        except ValueError as exc:
            print(f"❌ Invalid: {url} -> {exc}")