#!/usr/bin/env python3
"""
Utility to construct a fully-qualified URL for an external resource hosted on a CDN.

The function validates that the constructed URL points to one of the
allowed CDN domains and that the resource identifier is safe for use in a URL path.
"""

from __future__ import annotations

import re
import urllib.parse
from typing import Final, Set

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Example set of allowed CDN domains. Replace with your own.
ALLOWED_CDN_DOMAINS: Final[Set[str]] = {
    "cdn.example.com",
    "assets.myapp.net",
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _validate_domain(parsed_url: urllib.parse.ParseResult) -> None:
    """
    Ensure the URL's domain is in the allowed set.
    Raises ValueError if not allowed.
    """
    hostname = parsed_url.hostname
    if hostname is None or hostname.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not allowed for CDN access.")


def _validate_resource_id(resource_id: str) -> None:
    """
    Ensure the resource identifier contains only characters that are safe
    for use in a URL path component. Allowed: letters, digits, hyphen,
    underscore, dot.
    """
    if not re.match(r"^[A-Za-z0-9._-]+$", resource_id):
        raise ValueError(
            f"Invalid resource identifier '{resource_id}'. "
            "Only alphanumerics, '.', '-', and '_' are allowed."
        )


def _normalize_path(base_path: str, *segments: str) -> str:
    """
    Join path segments ensuring a single slash between them.
    Each segment is URL-encoded separately to avoid double encoding.
    """
    parts = [segment.strip("/") for segment in segments if segment]
    return "/".join([base_path.rstrip("/")] + parts)


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def construct_external_resource_url(
    cdn_base_url: str,
    resource_id: str,
    resource_type: str
) -> str:
    """
    Construct a secure URL to an external resource on the CDN.

    Parameters
    ----------
    cdn_base_url : str
        Base URL of the CDN (e.g., "https://cdn.example.com/assets").
    resource_id : str
        Identifier of the specific resource (e.g., "logo.png").
    resource_type : str
        Type/category of the resource (e.g., "image", "script").

    Returns
    -------
    str
        Fully-qualified URL pointing to the resource.

    Raises
    ------
    ValueError
        If the resulting URL points outside of the allowed CDN domains,
        or if the resource identifier contains unsafe characters.
    """
    # Parse and validate base URL
    parsed_base = urllib.parse.urlparse(cdn_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: '{cdn_base_url}'")

    _validate_domain(parsed_base)

    # Validate resource identifier
    _validate_resource_id(resource_id)

    # Ensure resource_type is a simple path component
    if not re.match(r"^[A-Za-z0-9._-]+$", resource_type):
        raise ValueError(
            f"Invalid resource type '{resource_type}'. "
            "Only alphanumerics, '.', '-', and '_' are allowed."
        )

    # Construct the final path
    resource_path = _normalize_path(parsed_base.path, resource_type, resource_id)

    # Rebuild the URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            resource_path,
            "",  # params
            "",  # query
            ""   # fragment
        )
    )

    # Final domain check (in case the path manipulation changed it)
    parsed_final = urllib.parse.urlparse(final_url)
    _validate_domain(parsed_final)

    return final_url


# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = construct_external_resource_url(
            "https://cdn.example.com/assets",
            "logo.png",
            "image"
        )
        print(url)
    except ValueError as exc:
        print(f"URL construction failed: {exc}")