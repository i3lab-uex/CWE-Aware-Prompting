#!/usr/bin/env python3
"""
Utility to safely construct a post‑login redirect URI.

The function ensures that the user supplied `next_route` cannot be used to
perform an open‑redirect attack.  It accepts either a relative path or a full URL.
If the supplied value is an absolute URL it must belong to one of the
`ALLOWED_DOMAINS`; otherwise a relative path is resolved against
`main_base_url`.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import urllib.parse as urlparse
from typing import Iterable, List


# --------------------------------------------------------------------------- #
# Configuration: allowed external domains for redirects.
# --------------------------------------------------------------------------- #
ALLOWED_DOMAINS: List[str] = [
    # Example external domains that are allowed.
    "example.com",
    "trustedpartner.org",
]

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _is_absolute(url: str) -> bool:
    """Return True if the URL has a scheme component."""
    return bool(urlparse.urlparse(url).scheme)


def _is_allowed_domain(netloc: str) -> bool:
    """Check whether the netloc (host[:port]) is in ALLOWED_DOMAINS."""
    host = netloc.split(":")[0].lower()
    return host in (d.lower() for d in ALLOWED_DOMAINS)


def _normalize_url(url: str) -> str:
    """
    Normalise a URL for comparison by stripping fragment and query components
    (which are irrelevant to the safety check).
    """
    parts = urlparse.urlparse(url)
    # Rebuild URL without fragment and query
    return urlparse.urlunparse(
        (parts.scheme, parts.netloc, parts.path, "", "", "")
    )


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def assemble_redirect_uri(main_base_url: str, next_route: str) -> str:
    """
    Construct a safe redirect URL after authentication.

    Parameters
    ----------
    main_base_url : str
        The base URL of the application (e.g., "https://app.example.com").
    next_route : str
        The user supplied route.  It may be a relative path (e.g.,
        "/dashboard") or an absolute URL.

    Returns
    -------
    str
        A fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is outside the base domain and not in
        `ALLOWED_DOMAINS`.
    """
    if not main_base_url:
        raise ValueError("main_base_url must be a non-empty string")

    # Resolve next_route relative to main_base_url if it is not absolute
    if _is_absolute(next_route):
        parsed_next = urlparse.urlparse(next_route)
        # If the URL has no scheme, treat it as relative
        if not parsed_next.scheme:
            next_route = urlparse.urljoin(main_base_url, next_route)
        else:
            # Absolute URL: ensure domain is allowed
            if not _is_allowed_domain(parsed_next.netloc):
                raise ValueError(
                    f"Redirect to external domain '{parsed_next.netloc}' is not allowed"
                )
            # If the absolute URL points to our own domain, ensure it's safe
            parsed_base = urlparse.urlparse(main_base_url)
            if parsed_next.netloc.lower() == parsed_base.netloc.lower():
                # Normalise to avoid duplicate slashes etc.
                next_route = _normalize_url(next_route)
    else:
        # Relative path: combine with base URL
        next_route = urlparse.urljoin(main_base_url, next_route)

    # Final safety check: ensure the resulting URL is within allowed scope
    final_parsed = urlparse.urlparse(next_route)
    base_parsed = urlparse.urlparse(main_base_url)

    # If the final URL points to our own domain, it's safe
    if final_parsed.netloc.lower() == base_parsed.netloc.lower():
        return next_route

    # Otherwise it must be in ALLOWED_DOMAINS
    if not _is_allowed_domain(final_parsed.netloc):
        raise ValueError(
            f"Redirect to external domain '{final_parsed.netloc}' is not allowed"
        )

    return next_route


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Basic tests
    base = "https://app.example.com"
    try:
        print(assemble_redirect_uri(base, "/dashboard"))  # safe relative
        print(assemble_redirect_uri(base, "https://example.com/page"))  # allowed domain
        print(assemble_redirect_uri(base, "http://malicious.com/"))  # should raise
    except ValueError as e:
        print(f"Security error: {e}")