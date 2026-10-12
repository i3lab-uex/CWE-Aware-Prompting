#!/usr/bin/env python3
"""
Utility to build a safe external resource URL for a CDN.

The function validates that the resulting URL points only to one of the
whitelisted CDN domains defined in ``ALLOWED_CDN_DOMAINS``.  This protects
against open‑redirect style attacks (CWE‑601) where a user could supply an
arbitrary URL that redirects to an untrusted domain.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import urllib.parse
from pathlib import Path
from typing import Iterable, Set

# --------------------------------------------------------------------------- #
# Whitelist of CDN domains that are considered safe.
# Replace the example entries with your actual allowed domains.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.contentprovider.org",
}

# --------------------------------------------------------------------------- #
def build_external_resource_link(
    cdn_url: str,
    resource_key: str,
    res_category: str,
) -> str:
    """
    Construct a full URL to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN (e.g., "https://cdn.example.com").
    resource_key : str
        Identifier for the specific resource (e.g., "logo.png").
    res_category : str
        Resource category or sub‑path (e.g., "images", "scripts").

    Returns
    -------
    str
        A fully qualified URL that points to the requested resource.

    Raises
    ------
    ValueError
        If the constructed URL does not resolve to an allowed CDN domain,
        or if any of the inputs are malformed.
    """
    # 1. Parse and validate the base CDN URL
    parsed_base = urllib.parse.urlparse(cdn_url)
    if parsed_base.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed_base.scheme!r}")

    base_netloc = parsed_base.netloc.lower()
    if base_netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Base CDN domain '{base_netloc}' is not in the allowed list."
        )

    # 2. Clean the category and key to avoid path traversal or double slashes
    clean_category = Path(res_category).as_posix().strip("/")
    clean_key = Path(resource_key).as_posix().strip("/")

    if not clean_category or not clean_key:
        raise ValueError("Resource category and key must be non‑empty strings.")

    # 3. Construct the relative path
    relative_path = f"/{clean_category}/{clean_key}"

    # 4. Join the base URL with the relative path
    full_url = urllib.parse.urljoin(cdn_url.rstrip("/") + "/", relative_path)

    # 5. Validate the resulting URL again (in case of manipulation)
    parsed_full = urllib.parse.urlparse(full_url)
    full_netloc = parsed_full.netloc.lower()
    if full_netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Constructed URL points to untrusted domain: {full_netloc!r}"
        )

    return full_url

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage
    try:
        url = build_external_resource_link(
            cdn_url="https://cdn.example.com",
            resource_key="logo.png",
            res_category="images"
        )
        print(f"Generated URL: {url}")
    except ValueError as exc:
        print(f"Error: {exc}")