#!/usr/bin/env python3
"""
Utility to build a validated CDN resource URL.

The function checks that the provided base URL belongs to an approved
CDN domain, sanitises the file identifier and type, then returns a fully
qualified URL suitable for fetching the resource.

Security considerations:
* Only URLs whose netloc is in ALLOWED_CDN_DOMAINS are accepted.
* The file_id and file_type must be alphanumeric (with optional
  dashes/underscores) to prevent path traversal or injection attacks.
* The scheme is preserved from the base URL; if missing, 'https' is
  assumed.
"""

from __future__ import annotations

import re
from urllib.parse import urlparse, urlunparse, quote_plus


# --------------------------------------------------------------------------- #
# Allowed CDN domains.  In a real project this would probably come from
# configuration or environment variables.
# --------------------------------------------------------------------------- #
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.another-cdn.net",
}


# --------------------------------------------------------------------------- #
# Validation helpers
# --------------------------------------------------------------------------- #
_FILE_ID_RE = re.compile(r"^[a-zA-Z0-9_\-]+$")  # simple safe pattern
_FILE_TYPE_RE = re.compile(r"^[a-zA-Z]+$")      # e.g., 'image', 'script'


def _validate_file_id(file_id: str) -> None:
    if not file_id or not _FILE_ID_RE.fullmatch(file_id):
        raise ValueError(f"Invalid file_id: {file_id!r}")


def _validate_file_type(file_type: str) -> None:
    if not file_type or not _FILE_TYPE_RE.fullmatch(file_type):
        raise ValueError(f"Invalid file_type: {file_type!r}")


def _validate_cdn_url_base(cdn_url_base: str) -> None:
    """
    Validate that the CDN base URL is absolute, uses HTTP(S),
    and points to an allowed domain.
    """
    parsed = urlparse(cdn_url_base)

    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"URL must use http or https scheme: {cdn_url_base!r}")

    if not parsed.netloc:
        raise ValueError(f"URL must contain a host: {cdn_url_base!r}")

    # Normalise the netloc (lowercase) and compare against allowed domains
    host = parsed.netloc.lower()
    if host not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Unauthorized CDN domain: {host!r}")


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def build_cdn_resource_url(cdn_url_base: str, file_id: str, file_type: str) -> str:
    """
    Assemble and validate a CDN resource URL.

    Parameters
    ----------
    cdn_url_base : str
        The base CDN URL (e.g., "https://cdn.example.com").
    file_id : str
        A unique identifier for the resource (e.g., "abc123").
    file_type : str
        The type/category of the resource (e.g., "image").

    Returns
    -------
    str
        A fully qualified, validated URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If any of the inputs are malformed or if the CDN domain is not allowed.
    """
    # Validate inputs
    _validate_cdn_url_base(cdn_url_base)
    _validate_file_id(file_id)
    _validate_file_type(file_type)

    # Parse the base URL to reconstruct a clean one
    parsed_base = urlparse(cdn_url_base)

    # Build the path: ensure no leading/trailing slashes in components
    path = f"/{quote_plus(file_type)}/{quote_plus(file_id)}"

    # Reconstruct the full URL
    final_url = urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            path,  # use our sanitized path
            "",    # params
            "",    # query
            "",    # fragment
        )
    )

    return final_url


# --------------------------------------------------------------------------- #
# Example usage (commented out to avoid execution during import)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        url = build_cdn_resource_url(
            "https://cdn.example.com",
            file_id="image_001.png",
            file_type="image"
        )
        print(url)  # https://cdn.example.com/image/image_001.png
    except ValueError as e:
        print(f"URL construction failed: {e}")