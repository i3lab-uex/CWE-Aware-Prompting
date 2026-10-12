#!/usr/bin/env python3
"""
Utility for safely constructing CDN resource URLs.

The module provides a single public function,
`generate_cdn_content_url`, which builds a full URL for a
resource (image, script, etc.) hosted on an approved CDN.
The implementation guards against open‑redirect attacks
(CWE‑601) by validating the resolved hostname against a whitelist.

Author: ChatGPT
"""

from __future__ import annotations

import posixpath
from urllib.parse import urlparse, urljoin, ParseResult


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# A whitelist of CDN domains that are considered safe.
# In a real application this would likely come from
# environment variables or configuration files.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "static.myapp.org",
    "assets.cdn.net",
}


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def generate_cdn_content_url(
    cdn_origin_url: str,
    content_id: str,
    content_kind: str,
) -> str:
    """
    Construct a fully qualified CDN URL for the given content.

    Parameters
    ----------
    cdn_origin_url : str
        Base URL of the CDN.  Example: ``https://cdn.example.com``.
    content_id : str
        Unique identifier for the resource.  Must be URL‑safe.
    content_kind : str
        Resource type (e.g., ``image`` or ``script``).

    Returns
    -------
    str
        A validated, absolute URL pointing to the resource on the CDN.

    Raises
    ------
    ValueError
        If the resolved URL points to a domain not present in
        :data:`ALLOWED_CDN_DOMAINS` or if any input is malformed.
    """

    # Basic sanity checks for the inputs
    if not cdn_origin_url:
        raise ValueError("cdn_origin_url must be a non‑empty string")
    if not content_id:
        raise ValueError("content_id must be a non‑empty string")
    if not content_kind:
        raise ValueError("content_kind must be a non‑empty string")

    # Parse the base URL and ensure it has a scheme and netloc
    parsed_base = urlparse(cdn_origin_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN origin URL: {cdn_origin_url!r}")

    # Normalize the base URL (strip any trailing slashes)
    normalized_base = parsed_base._replace(path=posixpath.normpath(parsed_base.path))
    base_url = normalized_base.geturl()

    # Build a safe relative path: /<kind>/<id>
    # Use posixpath to avoid '..' traversal or backslashes.
    safe_path = posixpath.join("/", content_kind, content_id)

    # Resolve the full URL
    candidate_url = urljoin(base_url.rstrip("/") + "/", safe_path.lstrip("/"))

    # Parse the resulting URL to validate its hostname
    parsed_candidate = urlparse(candidate_url)

    if not parsed_candidate.scheme or not parsed_candidate.netloc:
        raise ValueError(f"Generated URL is malformed: {candidate_url!r}")

    # Ensure the hostname is in the whitelist
    host = parsed_candidate.hostname.lower()
    if host not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Disallowed CDN domain: {host!r}. "
            f"Allowed domains are: {sorted(ALLOWED_CDN_DOMAINS)!r}"
        )

    # All checks passed; return the sanitized URL
    return candidate_url


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = generate_cdn_content_url(
            cdn_origin_url="https://cdn.example.com",
            content_id="12345.png",
            content_kind="image"
        )
        print("Generated URL:", url)
    except ValueError as exc:
        print("Error:", exc)