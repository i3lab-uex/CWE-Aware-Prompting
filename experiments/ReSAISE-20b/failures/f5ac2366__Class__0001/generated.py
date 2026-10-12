#!/usr/bin/env python3
"""
External Resource URL constructor.

This module provides a single function, `construct_external_resource_url`,
which safely builds URLs for fetching resources from a CDN.  The function
validates that the final URL resolves to an allowed domain and is
well‑formed, mitigating CWE‑610 (Externally Controlled Reference to a
Resource in Another Sphere).
"""

from __future__ import annotations

import re
from urllib.parse import urlparse, urljoin

# --------------------------------------------------------------------------- #
# Configuration: list of CDN domains that are trusted.  Add or remove as
# necessary for your deployment environment.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.example.net",
}

# Regular expression to validate resource identifiers (alphanumeric,
# hyphen, underscore).  Adjust the pattern if your CDN uses different
# naming conventions.
_RESOURCE_ID_RE = re.compile(r"^[a-zA-Z0-9_\-./]+$")

# --------------------------------------------------------------------------- #
def construct_external_resource_url(
    cdn_base_url: str,
    resource_id: str,
    resource_type: str,
) -> str:
    """
    Construct a fully qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base_url : str
        Base URL of the CDN, e.g. ``https://cdn.example.com``.
    resource_id : str
        Identifier of the requested resource, e.g. ``images/logo.png``.
    resource_type : str
        Logical type of the resource (e.g. ``image``, ``script``).  This
        value is not used for validation but can be helpful for debugging.

    Returns
    -------
    str
        A safe, absolute URL that points to the requested resource.

    Raises
    ------
    ValueError
        If any of the following conditions are true:
        * The CDN base URL is not a valid HTTP(S) URL.
        * The resulting domain is not in :data:`ALLOWED_CDN_DOMAINS`.
        * The resource identifier contains disallowed characters.
    """
    # Validate CDN base URL
    parsed_base = urlparse(cdn_base_url)
    if parsed_base.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed_base.scheme}'. Only HTTP/HTTPS are allowed.")
    if not parsed_base.netloc:
        raise ValueError("CDN base URL must contain a network location (domain).")

    # Ensure the CDN domain is allowed
    base_domain = parsed_base.netloc.lower()
    if base_domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{base_domain}' is not in the list of allowed CDN domains.")

    # Validate resource identifier
    if not _RESOURCE_ID_RE.match(resource_id):
        raise ValueError(f"Resource ID '{resource_id}' contains invalid characters.")

    # Prevent path traversal: normalize the path and ensure it stays within
    # a single level.  ``urljoin`` handles relative paths, but we also strip
    # any leading slashes to avoid overriding the base path.
    normalized_id = resource_id.lstrip("/")
    full_url = urljoin(parsed_base.geturl(), normalized_id)

    # Final domain check after join (in case of crafted inputs)
    parsed_full = urlparse(full_url)
    final_domain = parsed_full.netloc.lower()
    if final_domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Resulting URL domain '{final_domain}' is not allowed.")

    return full_url


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Simple demo usage
    try:
        url = construct_external_resource_url(
            cdn_base_url="https://cdn.example.com",
            resource_id="/images/logo.png",
            resource_type="image",
        )
        print(f"Constructed URL: {url}")
    except ValueError as exc:
        print(f"Error constructing URL: {exc}")