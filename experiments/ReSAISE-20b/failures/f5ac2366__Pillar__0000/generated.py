#!/usr/bin/env python3
"""
Utility to construct a secure CDN URL for external resources.

The function validates that the final URL points to an allowed CDN domain,
prevents path traversal, and normalises the resource type.

Author: ChatGPT
"""

from __future__ import annotations

import urllib.parse
from typing import Set

# --------------------------------------------------------------------------- #
# Configuration:  Allowed CDN domains.  Replace with real values in production.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.org",
    # Add other trusted CDN domains here.
}

# --------------------------------------------------------------------------- #
def construct_external_resource_url(
    cdn_base_url: str,
    resource_id: str,
    resource_type: str,
) -> str:
    """
    Construct a fully-qualified URL for an external resource on a CDN.

    Parameters
    ----------
    cdn_base_url : str
        Base URL of the CDN, e.g. "https://cdn.example.com".
    resource_id : str
        Identifier of the resource, e.g. "logo.png" or a UUID.
    resource_type : str
        Type of the resource, e.g. "image", "script", or "style".

    Returns
    -------
    str
        A normalised, fully-qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the final URL does not resolve to an allowed CDN domain or if
        any of the inputs are malformed.

    Notes
    -----
    The function protects against URL spoofing and path traversal attacks by:
        * Normalising the base URL.
        * Rejecting relative URLs for the resource ID.
        * Ensuring the domain is in ``ALLOWED_CDN_DOMAINS``.
    """
    # 1. Normalise the base URL
    parsed_base = urllib.parse.urlparse(cdn_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_base_url!r}")

    # 2. Verify the domain is allowed
    if parsed_base.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {parsed_base.hostname!r}")

    # 3. Sanitize the resource ID
    if not resource_id or ".." in resource_id:
        raise ValueError("Resource ID must be non-empty and cannot contain path traversal patterns.")

    # 4. Map resource_type to a subpath (optional). For demonstration, we simply
    #    prefix the path with the type; this can be customised as needed.
    subpath = urllib.parse.quote_plus(resource_type.strip().lower())
    # Ensure the resource ID is URL-encoded
    encoded_id = urllib.parse.quote_plus(resource_id.strip())

    # 5. Build the final path
    path = f"/{subpath}/{encoded_id}"
    # Combine with base URL
    final_url = urllib.parse.urljoin(parsed_base.geturl(), path)

    # 6. Final domain check after join (in case of weird inputs)
    parsed_final = urllib.parse.urlparse(final_url)
    if parsed_final.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Resulting URL points to disallowed domain: {parsed_final.hostname!r}")

    return final_url


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage
    try:
        url = construct_external_resource_url(
            "https://cdn.example.com",
            "logo.png",
            "image"
        )
        print(url)
    except ValueError as exc:
        print(f"Error: {exc}")