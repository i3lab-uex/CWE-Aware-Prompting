#!/usr/bin/env python3
"""
Utility to parse and validate URLs against a whitelist of allowed domains
and protocols, mitigating CWE‑441 (Confused Deputy) by ensuring the URL is
explicitly permitted before it can be used for outbound requests.
"""

from __future__ import annotations

import re
import urllib.parse
from typing import Final, Iterable


# --------------------------- Configuration -----------------------------------
ALLOWED_PROTOCOLS: Final[set[str]] = {"https", "http"}  # Extend as needed
# Domains that are allowed. Wildcard support (e.g., ".example.com") is provided.
ALLOWED_DOMAINS: Final[set[str]] = {
    "api.example.com",
    ".trustedpartner.org",   # matches subdomains of trustedpartner.org
}

# --------------------------- Helper Functions --------------------------------

def _is_domain_allowed(host: str) -> bool:
    """
    Check whether a host matches any of the allowed domain patterns.
    A pattern starting with '.' denotes a suffix match (subdomain support).
    """
    host = host.lower()
    for pattern in ALLOWED_DOMAINS:
        if pattern.startswith("."):
            # Suffix match (subdomain)
            if host.endswith(pattern.lower()):
                return True
        else:
            # Exact match
            if host == pattern.lower():
                return True
    return False


def _validate_scheme(scheme: str) -> bool:
    """
    Validate that the URL scheme is in the allowed list.
    """
    return scheme.lower() in ALLOWED_PROTOCOLS


# --------------------------- Main Function ----------------------------------

def parse_url(url: str) -> urllib.parse.ParseResult:
    """
    Parse a URL and validate its scheme and domain against predefined
    whitelists. Raises ValueError on invalid inputs.

    Parameters:
        url (str): The URL to be parsed.

    Returns:
        urllib.parse.ParseResult: The parsed URL object.

    Raises:
        ValueError: If the scheme or domain is not allowed.
    """
    if not isinstance(url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urllib.parse.urlparse(url)

    # Basic sanity checks
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include a scheme and network location")

    # Validate scheme
    if not _validate_scheme(parsed.scheme):
        raise ValueError(f"Scheme '{parsed.scheme}' is not allowed")

    # Extract host (without port)
    host_port = parsed.netloc.split("@")[-1]  # strip userinfo if present
    host = host_port.split(":")[0]            # strip port

    if not _is_domain_allowed(host):
        raise ValueError(f"Domain '{host}' is not in the allowed list")

    return parsed


# --------------------------- Example Usage ----------------------------------
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/resource",
        "http://sub.trustedpartner.org/path",
        "ftp://invalid.scheme.com/",
        "https://malicious.com/evil",
    ]

    for u in test_urls:
        try:
            result = parse_url(u)
            print(f"✅ {u} -> {result}")
        except ValueError as e:
            print(f"❌ {u} -> {e}")