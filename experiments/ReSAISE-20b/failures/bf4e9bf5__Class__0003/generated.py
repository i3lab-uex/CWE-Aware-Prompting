#!/usr/bin/env python3
"""
Utility to resolve an image URL only if it belongs to a trusted hosting domain.

The function protects against unintended proxy or intermediary issues by
ensuring that only URLs from a pre‑defined whitelist are accepted. Any
attempt to resolve a URL with an untrusted domain raises a ValueError.
"""

from __future__ import annotations

import re
from urllib.parse import urlparse, urlunparse, ParseResult


# --------------------------------------------------------------------------- #
# Trusted image hosting domains (add or remove as required)
# --------------------------------------------------------------------------- #
_TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trustedimage.org",
    "img.securehost.net",
}

# Regular expression to match a valid domain name (RFC 1035)
_DOMAIN_REGEX = re.compile(
    r"^(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}$"
)


def _is_valid_domain(domain: str) -> bool:
    """
    Check that the domain string is a syntactically valid hostname.
    """
    return bool(_DOMAIN_REGEX.match(domain))


def resolve_image_url(image_url: str) -> str:
    """
    Resolve the supplied image URL only if its domain is in the trusted list.

    Parameters
    ----------
    image_url : str
        The URL to validate and return unchanged if trusted.

    Returns
    -------
    str
        The original image URL if the domain is trusted.

    Raises
    ------
    ValueError
        If the URL's domain is not in the trusted list or if the URL is malformed.
    """
    # Parse the URL and ensure it has a scheme and network location
    parsed = urlparse(image_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {image_url!r}")

    # Normalise the domain to lower case for comparison
    hostname = parsed.hostname.lower() if parsed.hostname else ""

    # Basic domain validation to avoid DNS rebinding attacks
    if not _is_valid_domain(hostname):
        raise ValueError(f"Invalid domain name: {hostname!r}")

    # Check if the hostname is in the trusted list
    if hostname not in _TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {hostname!r}")

    # Re‑construct the URL to ensure consistent formatting
    safe_url = urlunparse(
        ParseResult(
            scheme=parsed.scheme,
            netloc=f"{hostname}:{parsed.port}" if parsed.port else hostname,
            path=parsed.path or "",
            params=parsed.params or "",
            query=parsed.query or "",
            fragment="",
        )
    )

    return safe_url