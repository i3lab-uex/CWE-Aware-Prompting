#!/usr/bin/env python3
"""
Secure URL redirect helper.

This module provides a single function, `validate_redirect_url`, which ensures
that any user‑supplied URL is safe to redirect to by checking its domain against
an approved list. The function raises a `ValueError` if the URL is not safe,
preventing unintended proxy or intermediary issues (CWE‑441).

Author: ChatGPT
"""

import re
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------------- #
# Approved domain list – edit as needed for your application.
# Only exact matches are allowed. Sub‑domains can be added explicitly if
# required (e.g., "example.com" does not match "sub.example.com").
# --------------------------------------------------------------------------- #
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "safe-site.net",
}

# --------------------------------------------------------------------------- #
# Regular expression to match a minimal, valid absolute URL.
# It allows http/https schemes and ensures at least one dot in the host part.
# --------------------------------------------------------------------------- #
_URL_RE = re.compile(
    r"^(?P<scheme>https?)://(?P<host>[^/]+)(?P<path>/.*)?$",
    re.IGNORECASE,
)

def _normalize_host(host: str) -> str:
    """
    Normalise the host component by stripping any port and converting to lower case.
    IPv6 addresses are left untouched (they are enclosed in brackets).
    """
    if host.startswith("[") and "]" in host:
        # IPv6 literal – strip port if present
        host_part, _, port = host.rpartition(":")
        return host_part.lower()
    # Regular hostname – strip port
    host_part, _, _ = host.partition(":")
    return host_part.lower()

def validate_redirect_url(input_url: str) -> str:
    """
    Validate a user‑supplied URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The URL supplied by the user.

    Returns
    -------
    str
        The validated, absolute URL that can be safely used for redirection.

    Raises
    ------
    ValueError
        If the URL is not absolute, uses an unsupported scheme,
        or its domain is not in the approved list.
    """
    # Ensure we have a string
    if not isinstance(input_url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(input_url)

    # Reject relative URLs and unsupported schemes
    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("URL must use http or https scheme")

    # Reject URLs without a network location (e.g., 'http:///path')
    if not parsed.netloc:
        raise ValueError("URL must contain a host")

    # Normalise the host (remove port, lower‑case)
    host = _normalize_host(parsed.netloc)

    # Verify the domain is approved
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for redirects")

    # Re‑construct the URL to ensure no unexpected fragments or queries
    safe_parts = (
        parsed.scheme.lower(),
        host,
        parsed.path or "",
        "",  # params
        "",  # query
        "",  # fragment
    )
    safe_url = urlunparse(safe_parts)

    return safe_url

# --------------------------------------------------------------------------- #
# Example usage (commented out; remove or adapt in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_urls = [
        "https://example.com/welcome",
        "http://trusted.org:8080/dashboard",
        "ftp://unsafe.net/file.txt",
        "/relative/path",
    ]

    for url in test_urls:
        try:
            print(f"Validating: {url}")
            safe = validate_redirect_url(url)
            print(f"  Safe URL: {safe}\n")
        except ValueError as e:
            print(f"  Error: {e}\n")