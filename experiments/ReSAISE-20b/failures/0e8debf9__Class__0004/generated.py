#!/usr/bin/env python3
"""
Safe redirect URI generator.

This module provides a single function, `generate_redirect_uri`, that builds
a full redirect URL after authentication.  The function ensures the target
URL is either relative to the application base URL or an absolute URL whose
hostname is explicitly whitelisted.

Author: ChatGPT
"""

from urllib.parse import urlparse, urlunparse, ParseResult
from typing import List

# --------------------------------------------------------------------------- #
# Configuration – adjust as appropriate for your application.
# --------------------------------------------------------------------------- #

# Base authentication URL (e.g., https://app.example.com)
AUTH_BASE_URL: str = "https://app.example.com"

# List of external domains that are allowed for post‑login redirects.
ALLOWED_DOMAINS: List[str] = [
    "dashboard.example.com",
    "external.partner.com",
]

# --------------------------------------------------------------------------- #
# Utility helpers
# --------------------------------------------------------------------------- #

def _is_absolute(url: str) -> bool:
    """
    Return True if the URL has a scheme (e.g., http:// or https://).
    """
    return bool(urlparse(url).scheme)

def _is_same_origin(base: str, target: str) -> bool:
    """
    Return True if the target URL has the same scheme and netloc as the base.
    """
    base_parsed = urlparse(base)
    target_parsed = urlparse(target)

    return (
        base_parsed.scheme.lower() == target_parsed.scheme.lower()
        and base_parsed.netloc.lower() == target_parsed.netloc.lower()
    )

def _is_allowed_external(url: str) -> bool:
    """
    Return True if the hostname of an absolute URL is in ALLOWED_DOMAINS.
    """
    hostname = urlparse(url).hostname
    if not hostname:
        return False
    # Normalize to lowercase for comparison
    hostname = hostname.lower()
    return any(hostname == allowed.lower() or hostname.endswith("." + allowed.lower())
               for allowed in ALLOWED_DOMAINS)

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def generate_redirect_uri(auth_base_url: str, post_login_param: str) -> str:
    """
    Construct a safe redirect URI.

    Parameters
    ----------
    auth_base_url : str
        The base URL of the application (e.g., "https://app.example.com").
    post_login_param : str
        The path or full URL supplied by the user to redirect to after login.

    Returns
    -------
    str
        The fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe (outside the base domain and not in
        ALLOWED_DOMAINS).
    """
    # Resolve relative paths against the base URL
    if not _is_absolute(post_login_param):
        # Build a new absolute URL using the base components
        base_parsed = urlparse(auth_base_url)
        # Ensure leading slash on the path
        relative_path = post_login_param if post_login_param.startswith("/") else "/" + post_login_param
        resolved_parsed = ParseResult(
            scheme=base_parsed.scheme,
            netloc=base_parsed.netloc,
            path=relative_path,
            params="",
            query="",
            fragment="",
        )
        resolved_url = urlunparse(resolved_parsed)
    else:
        # The user supplied an absolute URL; validate it
        resolved_url = post_login_param

    # Safety checks
    if _is_absolute(resolved_url):
        if not (_is_same_origin(auth_base_url, resolved_url) or _is_allowed_external(resolved_url)):
            raise ValueError(f"Unsafe redirect target: {resolved_url}")

    # Return the sanitized URL
    return resolved_url

# --------------------------------------------------------------------------- #
# Example usage (for debugging purposes)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        print(generate_redirect_uri(AUTH_BASE_URL, "/dashboard"))
        print(generate_redirect_uri(AUTH_BASE_URL, "https://external.partner.com/welcome"))
        # The following will raise ValueError
        print(generate_redirect_uri(AUTH_BASE_URL, "https://malicious.com/phish"))
    except ValueError as exc:
        print(f"Redirect rejected: {exc}")