#!/usr/bin/env python3
"""
Utility to construct a CDN resource URL while guarding against open‑redirect
and other security issues (CWE‑601).

The function validates that the resulting URL belongs to one of a predefined
set of allowed CDN domains. It also normalises the path and ensures that only
whitelisted resource types are accepted.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import re
from urllib.parse import urlparse, urljoin

# --------------------------------------------------------------------------- #
# Configuration – modify as appropriate for your environment
# --------------------------------------------------------------------------- #

ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.cdn.org",
}

# Regular expression to validate resource type (alphanumeric only)
_ALLOWED_RES_TYPES = re.compile(r"^(image|script)$", re.IGNORECASE)

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def create_resource_url(base_cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Build a fully‑qualified CDN URL for a given resource.

    Parameters
    ----------
    base_cdn_url : str
        Base URL of the CDN, e.g. ``https://cdn.example.com/``.
    res_id : str
        Unique identifier of the resource (typically a filename or hash).
    res_type : str
        Type of resource; must be one of the allowed values ('image' or 'script').

    Returns
    -------
    str
        Fully qualified URL pointing to the resource on a trusted CDN.

    Raises
    ------
    ValueError
        If any of the following occurs:
            * The constructed URL does not resolve to an allowed CDN domain.
            * ``res_type`` is not in the whitelist.
            * The base URL is malformed or missing a scheme.

    Notes
    -----
    - ``urljoin`` is used to correctly handle missing trailing slashes and
      relative paths.
    - The function normalises the path to avoid directory traversal attacks.
    """
    # --------------------------------------------------------------------- #
    # 1. Validate the resource type
    # --------------------------------------------------------------------- #
    if not _ALLOWED_RES_TYPES.match(res_type):
        raise ValueError(
            f"Invalid resource type '{res_type}'. Allowed types: image, script."
        )

    # --------------------------------------------------------------------- #
    # 2. Ensure base_cdn_url has a scheme and netloc
    # --------------------------------------------------------------------- #
    parsed_base = urlparse(base_cdn_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Malformed base CDN URL: {base_cdn_url!r}")

    # --------------------------------------------------------------------- #
    # 3. Construct the path component safely
    # --------------------------------------------------------------------- #
    # Prevent directory traversal by rejecting any leading ".." or absolute paths.
    safe_res_id = res_id.lstrip("./\\")
    if ".." in safe_res_id or safe_res_id.startswith(("/", "\\")):
        raise ValueError(f"Invalid resource identifier: {res_id!r}")

    # Create a relative path that incorporates the type for clarity
    rel_path = f"{res_type}s/{safe_res_id}"

    # --------------------------------------------------------------------- #
    # 4. Build the full URL
    # --------------------------------------------------------------------- #
    full_url = urljoin(base_cdn_url, rel_path)

    # --------------------------------------------------------------------- #
    # 5. Verify that the resulting domain is allowed
    # --------------------------------------------------------------------- #
    parsed_full = urlparse(full_url)
    if parsed_full.netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Domain '{parsed_full.netloc}' is not in the list of allowed CDN domains."
        )

    return full_url

# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        print(
            create_resource_url(
                base_cdn_url="https://cdn.example.com/",
                res_id="logo.png",
                res_type="image",
            )
        )
    except ValueError as exc:
        print(f"URL construction failed: {exc}")