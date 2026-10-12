#!/usr/bin/env python3
"""
Utility to safely construct URLs for external resources served from a CDN.

The function `generate_external_resource_url` validates that the provided
`cdn_base` resolves to a domain that is explicitly allowed and then builds
a well‑formed URL using the given resource identifier and type.  All user
supplied components are percent‑encoded to avoid injection attacks such as
CWE‑601 (open redirect) and other path traversal issues.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import urllib.parse
from typing import Set


# --------------------------------------------------------------------------- #
# Configuration: allowed CDN domains.  Replace or extend this set as needed.
# --------------------------------------------------------------------------- #
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "static-assets.cdn.net",
    "assets.myapp.org",
}


# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #
def generate_external_resource_url(cdn_base: str, res_id: str, res_type: str) -> str:
    """
    Construct a fully qualified URL pointing to an external resource hosted
    on a trusted CDN.

    Parameters
    ----------
    cdn_base : str
        The base URL of the CDN.  Must be an absolute URL (scheme + host).
    res_id : str
        Identifier for the resource.  May contain characters that need
        percent‑encoding.
    res_type : str
        Type of the resource (e.g., 'image', 'script').  Used as a path
        component and must be safe.

    Returns
    -------
    str
        A fully constructed URL that points to the requested resource.

    Raises
    ------
    ValueError
        If `cdn_base` resolves to a domain that is not in ``ALLOWED_CDN_DOMAINS``.
    """

    # --------------------------------------------------------------------- #
    # 1. Parse and validate the CDN base URL
    # --------------------------------------------------------------------- #
    parsed_base = urllib.parse.urlparse(cdn_base)

    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: '{cdn_base}'. Must be absolute.")

    # Ensure the host is in the allowed set
    if parsed_base.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"CDN domain '{parsed_base.hostname}' is not in the list of allowed domains."
        )

    # --------------------------------------------------------------------- #
    # 2. Percent‑encode the resource components
    # --------------------------------------------------------------------- #
    safe_res_type = urllib.parse.quote(res_type, safe="")
    safe_res_id = urllib.parse.quote(res_id, safe="")

    # --------------------------------------------------------------------- #
    # 3. Build the final URL
    # --------------------------------------------------------------------- #
    # Assemble path: /<res_type>/<res_id>
    path = f"/{safe_res_type}/{safe_res_id}"

    # Preserve any query or fragment from the base (unlikely but safe)
    final_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        path,
        "",  # params
        "",  # query
        "",  # fragment
    )
    final_url = urllib.parse.urlunparse(final_parts)

    return final_url


# --------------------------------------------------------------------------- #
# Example usage (for manual testing only)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        url = generate_external_resource_url(
            cdn_base="https://cdn.example.com",
            res_id="images/logo.png",
            res_type="image"
        )
        print(f"Generated URL: {url}")
    except ValueError as exc:
        print(f"Error: {exc}")