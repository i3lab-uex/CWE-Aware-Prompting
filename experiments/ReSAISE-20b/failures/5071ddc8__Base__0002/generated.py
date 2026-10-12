#!/usr/bin/env python3
"""
Safe redirect URI assembler.

This module provides a single function, `assemble_redirect_uri`, that safely
constructs a redirect URL after authentication. It guards against open‑redirect
vulnerabilities (CWE‑601) by validating that the target URL is either:

* a relative path within the same origin as `main_base_url`, or
* an absolute URL whose domain is explicitly whitelisted in
  ``ALLOWED_DOMAINS``.

If the target URL fails validation, a ``ValueError`` is raised.
"""

from __future__ import annotations

import urllib.parse
from typing import List


# --------------------------------------------------------------------------- #
# Configuration: allowed external domains for redirection
# --------------------------------------------------------------------------- #
ALLOWED_DOMAINS: List[str] = [
    "example.com",
    "trustedpartner.org",
    # Add other trusted domains here
]


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _is_absolute_url(url: str) -> bool:
    """
    Return True if *url* has a scheme and netloc (i.e., it is absolute).
    """
    parsed = urllib.parse.urlparse(url)
    return bool(parsed.scheme) and bool(parsed.netloc)


def _normalize_domain(domain: str) -> str:
    """
    Normalise a domain for comparison:

    * Lower‑case the domain.
    * Strip leading “www.” if present (optional but common).
    """
    domain = domain.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    return domain


def _is_domain_allowed(netloc: str, base_netloc: str) -> bool:
    """
    Return True if *netloc* is the same as *base_netloc* or
    is listed in ``ALLOWED_DOMAINS``.
    """
    if _normalize_domain(netloc) == _normalize_domain(base_netloc):
        return True

    # Check against the allowed list
    for allowed in ALLOWED_DOMAINS:
        if _normalize_domain(netloc) == _normalize_domain(allowed):
            return True
    return False


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def assemble_redirect_uri(main_base_url: str, next_route: str) -> str:
    """
    Safely construct a redirect URL.

    Parameters
    ----------
    main_base_url : str
        The base authentication URL of the application (e.g. ``https://app.example.com``).
    next_route : str
        The user‑supplied target URL or path.

    Returns
    -------
    str
        A fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe (i.e. points to an unapproved domain).
    """
    # Parse the base URL once
    base_parsed = urllib.parse.urlparse(main_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Invalid main_base_url: {main_base_url!r}")

    # If the user supplied a relative path, simply join it
    if not _is_absolute_url(next_route):
        # urljoin will handle relative paths, query strings, fragments, etc.
        resolved = urllib.parse.urljoin(main_base_url.rstrip("/") + "/", next_route.lstrip("/"))
    else:
        # Absolute URL: validate the domain
        target_parsed = urllib.parse.urlparse(next_route)
        if not _is_domain_allowed(target_parsed.netloc, base_parsed.netloc):
            raise ValueError(
                f"Redirect target domain '{target_parsed.netloc}' is not allowed"
            )
        # Normalise scheme and netloc (e.g., force https)
        target_parsed = target_parsed._replace(
            scheme=base_parsed.scheme,
            netloc=target_parsed.netloc,  # keep target domain
        )
        resolved = urllib.parse.urlunparse(target_parsed)

    return resolved


# --------------------------------------------------------------------------- #
# Example usage (commented out)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example base URL
    base = "https://app.example.com/login"

    # Safe relative path
    print(assemble_redirect_uri(base, "/dashboard"))

    # Safe absolute URL to a whitelisted domain
    print(assemble_redirect_uri(base, "https://trustedpartner.org/welcome"))

    # Unsafe absolute URL (will raise ValueError)
    try:
        print(assemble_redirect_uri(base, "https://malicious.com/steal"))
    except ValueError as exc:
        print(f"Security check failed: {exc}")