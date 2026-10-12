#!/usr/bin/env python3
"""
Secure URL redirection helper.

This module defines a single function `process_url_redirect` which accepts
a user‑supplied URL, validates that the domain is in an approved whitelist,
and returns a fully qualified, safe‑to‑use URL.  The implementation follows
common security guidelines and is resilient to several attack vectors,
including:

*   Redirection to malicious domains (CWE‑601)
*   URL parsing edge cases
*   Incomplete or malformed URLs

The function deliberately does **not** attempt to resolve DNS or verify
certificate chains; it simply ensures that the host part of the URL is in a
trusted set.  This keeps the function lightweight and avoids unnecessary
network calls while still providing strong safety guarantees.
"""

from __future__ import annotations

import re
import sys
from typing import Final, Iterable
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------------- #
# Configuration: a whitelist of fully qualified domain names that are
# considered safe for redirection.  The list can be expanded as needed.
# --------------------------------------------------------------------------- #
APPROVED_DOMAINS: Final[set[str]] = {
    "example.com",
    "trustedsite.org",
    "mycompany.net",
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_valid_scheme(scheme: str) -> bool:
    """Allow only http or https schemes."""
    return scheme.lower() in {"http", "https"}

def _normalize_domain(host: str) -> str:
    """
    Normalize a domain by stripping leading/trailing whitespace and converting
    to lowercase.  The function also removes any embedded port number.
    """
    host = host.strip().lower()
    # Remove :port if present
    return host.split(":")[0]

def _is_approved(host: str, approved_domains: Iterable[str]) -> bool:
    """
    Check if the host (or any of its parent domains) is in the approved set.
    For example, if "sub.example.com" is given and "example.com" is approved,
    this function returns True.
    """
    host_parts = host.split(".")
    # Iterate over progressively smaller suffixes
    for i in range(len(host_parts)):
        candidate = ".".join(host_parts[i:])
        if candidate in approved_domains:
            return True
    return False

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def process_url_redirect(input_url: str) -> str:
    """
    Validate a user‑supplied URL against an approved domain whitelist and
    return a safe, fully qualified redirect target.

    Parameters
    ----------
    input_url : str
        The URL supplied by the user.  It may be a relative path or an absolute
        URL.  If it is relative, the function will raise ValueError because a
        redirection target must be an absolute URL.

    Returns
    -------
    str
        A validated, fully qualified URL that is safe to redirect to.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme, or its domain
        is not in the approved list.
    """
    if not input_url:
        raise ValueError("input_url must be a non‑empty string")

    # Parse the URL
    parsed = urlparse(input_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"URL must be absolute and contain a scheme: '{input_url}'")

    if not _is_valid_scheme(parsed.scheme):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http/https are allowed.")

    # Normalize the host
    host = _normalize_domain(parsed.netloc)

    if not _is_approved(host, APPROVED_DOMAINS):
        raise ValueError(f"Domain '{host}' is not in the approved whitelist")

    # Reconstruct a clean URL (removing fragments and query if desired)
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return safe_url

# --------------------------------------------------------------------------- #
# Example usage (uncomment for manual testing)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_urls = [
        "https://example.com/path?query=1#frag",
        "http://sub.trustedsite.org/resource",
        "ftp://example.com/file",          # unsupported scheme
        "https://malicious.com/",           # unapproved domain
        "/relative/path",                  # relative URL
    ]

    for url in test_urls:
        try:
            result = process_url_redirect(url)
            print(f"✅ {url} -> {result}")
        except ValueError as exc:
            print(f"❌ {url} : {exc}", file=sys.stderr)