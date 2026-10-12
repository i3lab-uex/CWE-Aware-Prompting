#!/usr/bin/env python3
"""
Utility for generating a safe redirect URL after authentication.

The module provides `generate_redirect_uri`, which resolves a user-provided
redirect target against an authentication base URL while enforcing strict
security checks to prevent open redirect vulnerabilities.
"""

from urllib.parse import urlparse, urljoin
from typing import List

# --------------------------------------------------------------------------- #
# Configuration: a whitelist of external domains that are allowed for redirection
# --------------------------------------------------------------------------- #
ALLOWED_DOMAINS: List[str] = [
    "example.com",
    "trustedpartner.org",
    # Add other trusted domains here
]

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_allowed_domain(host: str) -> bool:
    """
    Return True if `host` is in the ALLOWED_DOMAINS list.
    Comparison is case-insensitive and ignores port numbers.
    """
    host = host.lower()
    # Strip possible port
    if ":" in host:
        host, _port = host.split(":", 1)
    return host in (d.lower() for d in ALLOWED_DOMAINS)

def _is_same_origin(base: str, target: str) -> bool:
    """
    Return True if `target` has the same scheme and netloc as `base`.
    """
    base_parsed = urlparse(base)
    target_parsed = urlparse(target)

    # Compare scheme (http/https) and netloc (host:port)
    return (
        base_parsed.scheme == target_parsed.scheme and
        base_parsed.netloc.lower() == target_parsed.netloc.lower()
    )

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def generate_redirect_uri(auth_base_url: str, post_login_param: str) -> str:
    """
    Resolve a user-provided redirect target against the authentication base URL.

    Parameters
    ----------
    auth_base_url : str
        The base authentication URL of the application (e.g., "https://app.example.com").
    post_login_param : str
        The URL path or full URL the user intends to navigate to after login.

    Returns
    -------
    str
        The fully-qualified redirect URL that is safe to use.

    Raises
    ------
    ValueError
        If the resolved URL points outside the allowed domains or is otherwise unsafe.
    """
    if not auth_base_url:
        raise ValueError("auth_base_url must be provided")

    # Normalize the base URL
    parsed_base = urlparse(auth_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("auth_base_url must be a valid absolute URL")

    # Resolve the target
    resolved = urljoin(auth_base_url, post_login_param)

    parsed_resolved = urlparse(resolved)

    # 1. Ensure the resolved URL has a scheme (http/https)
    if parsed_resolved.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed_resolved.scheme}")

    # 2. If the resolved URL is relative to the base (same origin), it's safe
    if _is_same_origin(auth_base_url, resolved):
        return resolved

    # 3. If the host is in ALLOWED_DOMAINS, allow it
    if parsed_resolved.netloc and _is_allowed_domain(parsed_resolved.netloc):
        return resolved

    # 4. Otherwise, reject the URL
    raise ValueError(f"Redirect URL '{resolved}' is not allowed (outside base domain and not in whitelist)")

# --------------------------------------------------------------------------- #
# Example usage
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Sample base URL and post-login parameter
    base = "https://app.example.com"
    next_param = "/dashboard?section=overview"

    try:
        redirect_url = generate_redirect_uri(base, next_param)
        print(f"Safe redirect URL: {redirect_url}")
    except ValueError as exc:
        print(f"Invalid redirect target: {exc}")