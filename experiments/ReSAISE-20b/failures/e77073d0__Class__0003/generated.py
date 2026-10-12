#!/usr/bin/env python3
"""
Utility for safely constructing CDN resource URLs.

The function ensures that the resulting URL points to a domain
that is explicitly allowed.  This mitigates CWE‑610 by preventing
externally controlled references from pointing to arbitrary hosts.
"""

from __future__ import annotations

import urllib.parse
from typing import Iterable, Set


# --------------------------------------------------------------------------- #
# Configuration: list of allowed CDN domains.
# These should be the exact hostnames that are trusted.
# --------------------------------------------------------------------------- #
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.prod.cdn.net",
}


def _is_allowed_domain(host: str) -> bool:
    """
    Check if the host part of a URL is in the whitelist.

    Parameters
    ----------
    host : str
        The hostname extracted from a URL (e.g., "cdn.example.com").

    Returns
    -------
    bool
        True if the host is in ``ALLOWED_CDN_DOMAINS``, False otherwise.
    """
    return host.lower() in ALLOWED_CDN_DOMAINS


def build_cdn_resource_url(
    cdn_url_base: str, file_id: str, file_type: str
) -> str:
    """
    Construct a fully qualified CDN URL for a given resource.

    Parameters
    ----------
    cdn_url_base : str
        The base URL of the CDN (e.g., "https://cdn.example.com/").
    file_id : str
        Unique identifier for the resource.
    file_type : str
        Resource type such as 'image', 'script', etc.

    Returns
    -------
    str
        The fully resolved, validated URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a host that is not in
        :data:`ALLOWED_CDN_DOMAINS`.
    """
    if not isinstance(cdn_url_base, str):
        raise TypeError("cdn_url_base must be a string")
    if not isinstance(file_id, str):
        raise TypeError("file_id must be a string")
    if not isinstance(file_type, str):
        raise TypeError("file_type must be a string")

    # Ensure the base ends with a slash to avoid path concatenation issues.
    if not cdn_url_base.endswith("/"):
        cdn_url_base += "/"

    # Build the relative path component.
    relative_path = urllib.parse.quote_plus(f"{file_type}/{file_id}")

    # Join base and relative path.
    full_url = urllib.parse.urljoin(cdn_url_base, relative_path)

    # Parse the resulting URL to extract hostname.
    parsed = urllib.parse.urlparse(full_url)
    host = parsed.hostname

    if host is None or not _is_allowed_domain(host):
        raise ValueError(
            f"Disallowed CDN domain: {host!r}. "
            f"Allowed domains are: {', '.join(sorted(ALLOWED_CDN_DOMAINS))}"
        )

    return full_url


# --------------------------------------------------------------------------- #
# Example usage (for demonstration only; remove or guard with __name__ == "__main__")
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        url = build_cdn_resource_url(
            "https://cdn.example.com/", file_id="12345", file_type="image"
        )
        print(f"Constructed URL: {url}")
    except Exception as e:
        print(f"Error: {e}")