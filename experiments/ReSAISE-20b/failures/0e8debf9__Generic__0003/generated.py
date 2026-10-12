#!/usr/bin/env python3
"""
Utility for generating a safe redirect URL after authentication.

The function validates that the target location is either:
* within the same origin as ``auth_base_url``; or
* a fully-qualified URL whose hostname is listed in ``ALLOWED_DOMAINS``.

Any other target results in a ValueError.
"""

from __future__ import annotations

import sys
from urllib.parse import urlparse, urljoin, ParseResult

# Pre‑approved external domains for redirection.
ALLOWED_DOMAINS = {
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed
}


def generate_redirect_uri(auth_base_url: str, post_login_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    auth_base_url : str
        The base authentication URL of the application (e.g. ``https://app.example.com``).
    post_login_param : str
        The user‑supplied path or full URL to redirect to after login.

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the same origin as ``auth_base_url``
        and its hostname is not in :data:`ALLOWED_DOMAINS`.
    """
    # Parse the base URL once
    base_parsed = urlparse(auth_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Invalid auth_base_url: {auth_base_url!r}")

    # Resolve the target URL relative to the base
    joined = urljoin(auth_base_url, post_login_param)
    target_parsed: ParseResult = urlparse(joined)

    # If the target URL is relative (no scheme/netloc) it will inherit from base
    if not target_parsed.scheme:
        # urljoin guarantees scheme/netloc will be present, but check anyway
        target_parsed = target_parsed._replace(
            scheme=base_parsed.scheme, netloc=base_parsed.netloc
        )

    # Safety check: same origin or allowed domain
    if target_parsed.netloc != base_parsed.netloc:
        # Extract hostname (exclude port)
        host = target_parsed.hostname or ""
        if host not in ALLOWED_DOMAINS:
            raise ValueError(
                f"Unsafe redirect target: {joined!r} not in allowed domains"
            )

    # Reconstruct the URL to ensure consistency
    safe_url = target_parsed.geturl()
    return safe_url


# -------------------------------------------------------------
# Example usage (uncomment to test manually)
# -------------------------------------------------------------
if __name__ == "__main__":
    try:
        base = "https://app.example.com"
        # Relative path
        print(generate_redirect_uri(base, "/dashboard"))
        # Absolute URL within same domain
        print(generate_redirect_uri(base, "https://app.example.com/profile"))
        # Absolute URL to allowed external domain
        print(generate_redirect_uri(base, "https://trustedpartner.org/welcome"))
        # Unsafe external domain (should raise)
        print(generate_redirect_uri(base, "https://evil.com/hack"))
    except ValueError as e:
        print(f"Security error: {e}", file=sys.stderr)