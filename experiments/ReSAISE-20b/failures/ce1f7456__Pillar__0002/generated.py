#!/usr/bin/env python3
"""
Secure URL redirection helper.

The function validates the destination URL against a whitelist of safe domains,
ensures that only http/https schemes are allowed, and returns a sanitized URL
ready for redirection.  It raises ValueError when the destination is not
trusted.

Author: ChatGPT
"""

from __future__ import annotations

import re
from urllib.parse import urlparse, urlunparse, ParseResult


# A set of domains that are considered safe for redirection.
ALLOWED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.local",
}

# Regular expression to validate the scheme (http or https).
_SCHEME_RE = re.compile(r"^(https?)$", re.IGNORECASE)


def _is_allowed_domain(netloc: str) -> bool:
    """
    Check if the given network location (netloc) is within ALLOWED_DOMAINS.
    Handles subdomains by allowing only exact matches for simplicity.
    """
    # Strip any port number
    host = netloc.split(":")[0].lower()
    return host in ALLOWED_DOMAINS


def _sanitize_url(parsed: ParseResult) -> str:
    """
    Reconstruct a URL from its parsed components, removing fragments
    and query parameters that might be used for phishing or other attacks.
    """
    # Preserve scheme, netloc, path; drop params, query, fragment
    sanitized = ParseResult(
        scheme=parsed.scheme,
        netloc=parsed.netloc,
        path=parsed.path or "/",
        params="",
        query="",
        fragment="",
    )
    return urlunparse(sanitized)


def secure_url_redirect(destination_url: str) -> str:
    """
    Validate and sanitize a user-provided URL for safe redirection.

    Parameters
    ----------
    destination_url : str
        The raw URL provided by the user.

    Returns
    -------
    str
        A sanitized URL that is guaranteed to be within the allowed domains.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        or its domain is not in ALLOWED_DOMAINS.
    """
    if not destination_url:
        raise ValueError("Destination URL must not be empty")

    # Parse the URL
    parsed = urlparse(destination_url)

    # Validate scheme
    if not _SCHEME_RE.match(parsed.scheme):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Validate domain
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain)")

    if not _is_allowed_domain(parsed.netloc):
        raise ValueError(f"Domain {parsed.netloc!r} is not allowed for redirection")

    # Sanitize the URL
    sanitized = _sanitize_url(parsed)
    return sanitized


# Example usage (for testing purposes only; remove or guard with __name__ == "__main__")
if __name__ == "__main__":
    test_urls = [
        "https://example.com/path?query=123#frag",
        "http://trustedsite.org/anotherpath/",
        "https://malicious.com/hack",
        "ftp://example.com/resource",
    ]

    for url in test_urls:
        try:
            print(f"Original: {url}")
            print(f"Sanitized: {secure_url_redirect(url)}\n")
        except ValueError as exc:
            print(f"Rejected: {exc}\n")