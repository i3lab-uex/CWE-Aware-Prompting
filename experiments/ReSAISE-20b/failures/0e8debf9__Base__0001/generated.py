#!/usr/bin/env python3
"""
Utility to safely generate a post‑login redirect URI.

The function ensures that the user supplied `post_login_param` does not
cause an open redirect.  Only URLs that are either relative to the
authentication base URL or point to a domain in the `ALLOWED_DOMAINS`
list are accepted.  Any other value raises a ValueError.
"""

from urllib.parse import urlparse, urljoin
from typing import List

# --------------------------------------------------------------------------- #
# Configuration: list of external domains that are permitted for redirection.
# These should be fully qualified domain names, e.g. "example.com".
ALLOWED_DOMAINS: List[str] = [
    # Add any domains you trust for post‑login redirects here.
    "trusted.example.com",
    "another.trusted.org",
]

# --------------------------------------------------------------------------- #
def _is_allowed_domain(netloc: str) -> bool:
    """
    Return True if the netloc (host[:port]) is in ALLOWED_DOMAINS.
    """
    host = netloc.split(":")[0].lower()
    return host in (d.lower() for d in ALLOWED_DOMAINS)


def generate_redirect_uri(auth_base_url: str, post_login_param: str) -> str:
    """
    Construct a safe redirect URI for use after authentication.

    Parameters
    ----------
    auth_base_url : str
        The base URL of the application (e.g. "https://app.example.com").
    post_login_param : str
        The user supplied path or full URL to redirect to after login.

    Returns
    -------
    str
        A fully resolved absolute URI safe for redirection.

    Raises
    ------
    ValueError
        If the resolved URL is not safe (e.g. points to an untrusted domain).
    """
    if not auth_base_url:
        raise ValueError("auth_base_url must be a non-empty string")

    # Parse the base URL to extract its components
    base_parsed = urlparse(auth_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("auth_base_url must be a valid absolute URL")

    # Resolve the user supplied parameter against the base
    resolved = urljoin(auth_base_url, post_login_param)

    parsed_resolved = urlparse(resolved)

    # 1. If the resolved URL is relative (no scheme), prepend base
    if not parsed_resolved.scheme:
        # urljoin already handled this, but we double‑check
        resolved = urljoin(auth_base_url, post_login_param)
        parsed_resolved = urlparse(resolved)

    # 2. If the resolved URL is absolute, validate scheme and host
    if parsed_resolved.scheme in ("http", "https"):
        # If the host matches the auth base domain, allow it
        if parsed_resolved.netloc.lower() == base_parsed.netloc.lower():
            return resolved

        # Otherwise, check against the allowed external domains list
        if _is_allowed_domain(parsed_resolved.netloc):
            return resolved

    # Anything else is considered unsafe
    raise ValueError(f"Unsafe redirect URL: {resolved}")


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Simple demo / sanity check
    try:
        print(generate_redirect_uri(
            "https://app.example.com",
            "/dashboard"
        ))  # => https://app.example.com/dashboard

        print(generate_redirect_uri(
            "https://app.example.com",
            "https://trusted.example.com/welcome"
        ))  # => https://trusted.example.com/welcome

        # This will raise ValueError
        print(generate_redirect_uri(
            "https://app.example.com",
            "http://evil.badsite.net/phish"
        ))
    except ValueError as exc:
        print(f"Redirect rejected: {exc}")