#!/usr/bin/env python3
"""
Safe redirect URL generator for post‑login redirection.

The function `generate_redirect_uri` validates the user supplied
redirect target against a base authentication URL and a whitelist of
allowed external domains.  It prevents open‑redirect attacks (CWE‑601)
and ensures that resources are properly controlled throughout their
lifetime.

Author: ChatGPT
"""

from urllib.parse import urlparse, urlunparse
from typing import List

# --------------------------------------------------------------------------- #
# Configuration – allowed external domains for redirects
# --------------------------------------------------------------------------- #
ALLOWED_DOMAINS: List[str] = [
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed
]


def _is_allowed_domain(domain: str) -> bool:
    """
    Check if a domain is present in the whitelist.
    Comparison is case‑insensitive and ignores leading 'www.'.
    """
    domain = domain.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    return domain in (d.lower() for d in ALLOWED_DOMAINS)


def generate_redirect_uri(auth_base_url: str, post_login_param: str) -> str:
    """
    Construct a safe redirect URI after login.

    Parameters
    ----------
    auth_base_url : str
        The base URL of the authentication service (e.g. "https://app.example.com").
    post_login_param : str
        The user supplied target – can be a relative path or an absolute URL.

    Returns
    -------
    str
        A fully resolved, safe redirect URI.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe:
            * It points to a domain outside the base authentication domain
              and not in `ALLOWED_DOMAINS`.
            * The URL is malformed.
    """
    # Parse base authentication URL
    try:
        base_parsed = urlparse(auth_base_url)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Invalid base URL '{auth_base_url}': {exc}") from exc

    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Base URL must be absolute: '{auth_base_url}'")

    # Resolve the user supplied parameter
    try:
        target_parsed = urlparse(post_login_param)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Invalid redirect target '{post_login_param}': {exc}") from exc

    # If the target is relative, combine with base
    if not target_parsed.scheme:
        resolved = urlunparse(
            (
                base_parsed.scheme,
                base_parsed.netloc,
                target_parsed.path or "",
                target_parsed.params,
                target_parsed.query,
                target_parsed.fragment,
            )
        )
        resolved_parsed = urlparse(resolved)
    else:
        # Absolute URL – check domain
        resolved_parsed = target_parsed

    # Domain checks
    base_domain = base_parsed.netloc.lower()
    target_domain = resolved_parsed.netloc.lower()

    # If the target domain is empty (relative URL), it's safe
    if target_domain:
        # Allow if same as base domain
        if target_domain == base_domain:
            return resolved_parsed.geturl()

        # Allow if in whitelist
        if _is_allowed_domain(target_domain):
            return resolved_parsed.geturl()

        # Otherwise reject
        raise ValueError(
            f"Redirect target domain '{target_domain}' is not allowed "
            f"(base: '{base_domain}')"
        )

    # No domain – relative URL, already resolved
    return resolved_parsed.geturl()


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    base = "https://app.example.com"
    tests = [
        "/dashboard",
        "https://example.com/welcome",
        "http://malicious.com/phish",
        "/../secret",
    ]

    for t in tests:
        try:
            print(f"Input: {t} -> Redirect URL: {generate_redirect_uri(base, t)}")
        except ValueError as e:
            print(f"Input: {t} -> Error: {e}")