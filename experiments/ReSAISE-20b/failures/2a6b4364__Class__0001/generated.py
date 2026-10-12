#!/usr/bin/env python3
"""
Secure redirect URL generator.

This module provides a single function, `create_redirect_url`, which safely
constructs a redirect URL after successful login.  The function ensures that
the final URL is either within the same domain as `base_url` or belongs to a
pre‑approved list of external domains (`ALLOWED_DOMAINS`).  Any attempt to
redirect the user to an arbitrary domain will raise a `ValueError`.

The implementation follows best practices for preventing open redirect
vulnerabilities (CWE‑601) and externally controlled references (CWE‑610).
"""

from urllib.parse import urlparse, urljoin
import re

# --------------------------------------------------------------------------- #
# Configuration: list of external domains that are allowed for redirection.
# These should be fully qualified domain names (FQDNs) without protocol or
# path components.  Example: ['example.com', 'trusted.org']
ALLOWED_DOMAINS = [
    # Add allowed external domains here
]

# --------------------------------------------------------------------------- #
def _is_allowed_domain(host: str) -> bool:
    """
    Determine whether a host is allowed for redirection.

    Parameters
    ----------
    host : str
        The hostname component of a URL (e.g. "sub.example.com").

    Returns
    -------
    bool
        True if the host is either the same as `base_url`'s host or ends with
        one of the domains listed in ALLOWED_DOMAINS.
    """
    # Normalize host: strip port if present
    host = host.split(':')[0].lower()
    # Check for exact match with allowed domains
    return any(host == d.lower() or host.endswith('.' + d.lower())
               for d in ALLOWED_DOMAINS)

# --------------------------------------------------------------------------- #
def create_redirect_url(base_url: str, next_param: str) -> str:
    """
    Safely construct a redirect URL.

    Parameters
    ----------
    base_url : str
        The application's base URL (e.g. "https://app.example.com/").
    next_param : str
        The user‑supplied value for the "next" parameter.

    Returns
    -------
    str
        The fully resolved redirect URL that is safe to use.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is neither the same as
        `base_url` nor listed in ALLOWED_DOMAINS.
    """
    if not isinstance(base_url, str) or not isinstance(next_param, str):
        raise TypeError("Both base_url and next_param must be strings.")

    # Parse the base URL to extract its components
    parsed_base = urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base_url: {base_url!r}")

    # Join the next_param to the base URL.  This handles relative paths,
    # query strings, and fragments correctly.
    candidate_url = urljoin(base_url, next_param)

    # Parse the resulting URL to examine its host
    parsed_candidate = urlparse(candidate_url)
    candidate_host = parsed_candidate.netloc.split(':')[0].lower()

    # If the candidate is an absolute URL with a different host, ensure
    # it is allowed.
    if parsed_candidate.scheme and candidate_host != parsed_base.netloc.split(':')[0].lower():
        if not _is_allowed_domain(candidate_host):
            raise ValueError(
                f"Redirect to external domain '{candidate_host}' is not allowed."
            )

    # If the candidate URL is relative (no scheme/netloc), it's safe.
    return candidate_url

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage and simple test cases
    base = "https://app.example.com/"
    tests = [
        "/dashboard",
        "profile?tab=info",
        "../logout",
        "https://app.example.com/admin",          # same domain
        "https://trusted.org/welcome",             # allowed external
        "http://malicious.com/steal?data=123"      # disallowed external
    ]

    for nxt in tests:
        try:
            print(f"next: {nxt!r} -> redirect: {create_redirect_url(base, nxt)!r}")
        except ValueError as e:
            print(f"next: {nxt!r} -> ERROR: {e}")