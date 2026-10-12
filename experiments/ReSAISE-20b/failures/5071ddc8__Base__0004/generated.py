#!/usr/bin/env python3
"""
Utility to safely assemble a redirect URL after authentication.

The function validates the user supplied `next_route` ensuring it does not
lead to an untrusted domain (CWE‑601: Open Redirect).  Only URLs that are
relative to the application's base or belong to a whitelisted domain are
accepted.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

from urllib.parse import urlparse, urljoin
from typing import List


# --------------------------------------------------------------------------- #
# Configuration – list of domains that are allowed for external redirects.
# --------------------------------------------------------------------------- #
ALLOWED_DOMAINS: List[str] = [
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed
]


def assemble_redirect_uri(main_base_url: str, next_route: str) -> str:
    """
    Construct a safe redirect URL based on the application's base URL and
    a user supplied path or absolute URL.

    Parameters
    ----------
    main_base_url : str
        The base authentication URL of the application (e.g. https://app.example.com).
    next_route : str
        The user supplied redirect target – can be a relative path or a full URL.

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe: it points to a domain that is neither
        the application's base domain nor one of the explicitly allowed external domains.
    """
    if not main_base_url:
        raise ValueError("main_base_url must be a non-empty string")

    # Parse the base URL to extract its components
    base_parsed = urlparse(main_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Invalid main_base_url: {main_base_url!r}")

    # Resolve the next_route against the base URL
    resolved = urljoin(main_base_url, next_route)

    # Parse the resolved URL to inspect its components
    parsed = urlparse(resolved)

    # Ensure scheme is HTTP(S) – reject others like javascript:, data:, etc.
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # If the hostname matches the base domain, it's safe
    if parsed.hostname and parsed.hostname.lower() == base_parsed.hostname.lower():
        return resolved

    # If the hostname is in the whitelist, it's also safe
    if parsed.hostname and parsed.hostname.lower() in (d.lower() for d in ALLOWED_DOMAINS):
        return resolved

    # Anything else is considered unsafe
    raise ValueError(
        f"Redirect to untrusted domain '{parsed.hostname}' is not allowed"
    )


# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Test cases
    base = "https://app.example.com"

    try:
        print(assemble_redirect_uri(base, "/dashboard"))
        print(assemble_redirect_uri(base, "https://example.com/profile"))
        print(assemble_redirect_uri(base, "https://malicious.com/steal"))
    except ValueError as exc:
        print(f"Redirect blocked: {exc}")