#!/usr/bin/env python3
"""
Secure user redirect helper.

This module defines a single function, `secure_user_redirect`, which validates
a user supplied URL against a whitelist of approved domains before allowing it
to be used for redirection.  The function protects against open‑redirect
vulnerabilities and the CWE‑441 “Confused Deputy” problem by ensuring that the
URL is absolute, uses a safe scheme (http/https), and belongs to one of the
approved hosts.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import re
from urllib.parse import urlparse, ParseResult


# --------------------------------------------------------------------------- #
# Configuration: list of approved external domains
# --------------------------------------------------------------------------- #
# Example entries.  Add or remove hosts as appropriate for your application.
APPROVED_DOMAINS = {
    "example.com",
    "trustedpartner.org",
    "secure.example.net",
}


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _is_valid_scheme(parsed: ParseResult) -> bool:
    """Return True if the URL scheme is http or https."""
    return parsed.scheme in ("http", "https")


def _extract_domain(parsed: ParseResult) -> str:
    """
    Extract the registered domain (excluding subdomains) from a parsed URL.
    For simplicity, we use a regex that matches the last two parts of the host.
    """
    # Normalize to lower case
    hostname = parsed.hostname or ""
    hostname = hostname.lower()

    # Use a simple regex to capture the last two labels.
    match = re.search(r"([a-z0-9.-]+\.[a-z]{2,})$", hostname)
    return match.group(1) if match else ""


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def secure_user_redirect(url_input: str) -> str:
    """
    Validate a user supplied URL against the approved domain list.

    Parameters
    ----------
    url_input : str
        The raw URL string supplied by the user.

    Returns
    -------
    str
        A sanitized, absolute URL that can safely be used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsafe scheme, or its domain is not
        in the approved list.
    """
    if not isinstance(url_input, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(url_input)

    # Reject relative URLs or missing scheme
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute and include a scheme")

    # Only allow http/https
    if not _is_valid_scheme(parsed):
        raise ValueError("Only HTTP and HTTPS URLs are allowed")

    # Extract the domain (excluding subdomains) for whitelist comparison
    domain = _extract_domain(parsed)
    if not domain:
        raise ValueError("Unable to determine the domain of the URL")

    # Case‑insensitive comparison
    if domain.lower() not in {d.lower() for d in APPROVED_DOMAINS}:
        raise ValueError(f"Domain '{domain}' is not approved for redirection")

    # Re‑construct the URL to avoid any tampering (e.g., missing slashes)
    safe_url = parsed.geturl()

    return safe_url


# --------------------------------------------------------------------------- #
# Example usage (for manual testing)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_urls = [
        "https://example.com/path?query=1",
        "http://sub.trustedpartner.org/resource",
        "https://malicious.com/evil",
        "/relative/path",
    ]

    for url in test_urls:
        try:
            print(f"Safe URL: {secure_user_redirect(url)}")
        except ValueError as exc:
            print(f"Rejected URL '{url}': {exc}")