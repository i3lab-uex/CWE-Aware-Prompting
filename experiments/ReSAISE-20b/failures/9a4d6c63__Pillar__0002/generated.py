#!/usr/bin/env python3
"""
A small utility to parse URLs with strict validation.

The function :func:`parse_url` ensures that the URL uses an allowed
protocol and domain before returning a ``urllib.parse.ParseResult``.
It raises :class:`ValueError` for any disallowed scheme or domain.

The implementation protects against common security pitfalls such as
unexpected protocols (e.g. ``file://``) and ensures that the returned
object is fully resolved (i.e., the netloc is a valid hostname).
"""

from __future__ import annotations

import re
import socket
from urllib.parse import urlparse, ParseResult
from typing import Iterable

# --------------------------------------------------------------------------- #
# Configuration: allowed schemes and domains.  Adjust these sets as needed.
# --------------------------------------------------------------------------- #

ALLOWED_SCHEMES: frozenset[str] = frozenset({"http", "https"})
ALLOWED_DOMAINS: frozenset[str] = frozenset(
    {
        "example.com",
        "api.example.org",
        # Add more allowed domains here.
    }
)

# Regular expression for a valid hostname (RFC 1035)
HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
)

def _is_valid_hostname(hostname: str) -> bool:
    """
    Validate a hostname according to RFC 1035.

    Args:
        hostname: The host part of the URL.

    Returns:
        True if the hostname is syntactically valid, False otherwise.
    """
    return bool(HOSTNAME_RE.match(hostname))


def _resolve_hostname(hostname: str) -> None:
    """
    Resolve the hostname to ensure it actually exists.
    This prevents typos or malicious URLs that point to non-existent hosts.

    Args:
        hostname: The host part of the URL.

    Raises:
        ValueError: If the hostname cannot be resolved.
    """
    try:
        socket.gethostbyname(hostname)
    except socket.gaierror as exc:  # pragma: no cover
        raise ValueError(f"Hostname '{hostname}' could not be resolved") from exc


def parse_url(url: str) -> ParseResult:
    """
    Parse a URL and validate its scheme and domain.

    The function checks that:
      * the scheme is in :data:`ALLOWED_SCHEMES`;
      * the hostname matches a valid pattern and is resolvable;
      * the hostname ends with one of :data:`ALLOWED_DOMAINS`.

    Args:
        url: The URL string to parse.

    Returns:
        A :class:`urllib.parse.ParseResult` object representing the parsed URL.

    Raises:
        ValueError: If the scheme or domain is not allowed, if the hostname
            is malformed, or if the hostname cannot be resolved.
    """
    # Step 1: Basic parsing
    parsed = urlparse(url)

    # Scheme validation
    if not parsed.scheme:
        raise ValueError("URL must include a scheme (e.g., http://)")
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(
            f"Scheme '{parsed.scheme}' is not allowed. "
            f"Allowed schemes: {', '.join(sorted(ALLOWED_SCHEMES))}"
        )

    # Netloc (hostname) validation
    hostname = parsed.hostname  # type: ignore[assignment]
    if not hostname:
        raise ValueError("URL must include a valid host component")

    # Normalize to lower case for comparison
    hostname_lc = hostname.lower()

    if not _is_valid_hostname(hostname_lc):
        raise ValueError(f"Hostname '{hostname}' is not a valid domain name")

    # Domain whitelist check (allow subdomains of the allowed domains)
    if not any(hostname_lc.endswith("." + domain) or hostname_lc == domain
               for domain in ALLOWED_DOMAINS):
        raise ValueError(
            f"Domain '{hostname}' is not in the list of allowed domains: "
            f"{', '.join(sorted(ALLOWED_DOMAINS))}"
        )

    # Optional: Resolve hostname to catch typos or DNS issues
    _resolve_hostname(hostname_lc)

    # All checks passed – return the parsed URL object
    return parsed


# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to run):
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_urls = [
        "https://api.example.org/v1/resource",
        "http://example.com:8080/path?query=param#fragment",
        # The following should raise ValueError
        "ftp://example.com/resource",
        "https://malicious.badsite.org/",
    ]

    for u in test_urls:
        try:
            result = parse_url(u)
            print(f"Parsed: {result}")
        except ValueError as e:
            print(f"Failed to parse '{u}': {e}")