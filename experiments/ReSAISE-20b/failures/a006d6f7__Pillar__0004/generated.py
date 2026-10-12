#!/usr/bin/env python3
"""
Utility for constructing secure CDN resource URLs.
"""

from __future__ import annotations

import posixpath
import urllib.parse
from typing import Iterable

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# A set of fully-qualified domains that are allowed to serve content.
ALLOWED_CDN_DOMAINS: set[str] = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.cdn.net",
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _sanitize_path_component(component: str) -> str:
    """
    Ensure a path component does not contain disallowed characters
    (e.g. slashes, leading dots) that could be used for path traversal.
    """
    if not component:
        raise ValueError("Content identifier cannot be empty.")
    if "/" in component or "\\" in component:
        raise ValueError("Content identifier must not contain slashes.")
    if component.startswith("."):
        raise ValueError("Content identifier cannot start with a dot.")
    return component

def _validate_domain(netloc: str) -> None:
    """
    Verify that the domain (netloc) is in the list of allowed CDN domains.
    """
    if netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Unauthorized CDN domain: {netloc}")

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def generate_cdn_content_url(
    cdn_origin_url: str,
    content_id: str,
    content_kind: str,
) -> str:
    """
    Construct a fully-qualified URL for a CDN resource.

    Parameters
    ----------
    cdn_origin_url : str
        The base URL of the CDN, e.g. "https://cdn.example.com/"
    content_id : str
        A unique identifier for the resource (must be a single path component).
    content_kind : str
        The type/category of the resource (e.g. "image", "script").

    Returns
    -------
    str
        A validated, absolute URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain not in ``ALLOWED_CDN_DOMAINS``
        or if the identifiers contain disallowed characters.
    """
    # Parse the origin URL to ensure it is well-formed
    parsed_origin = urllib.parse.urlparse(cdn_origin_url)
    if not parsed_origin.scheme or not parsed_origin.netloc:
        raise ValueError("Invalid CDN origin URL")

    # Validate that the domain is permitted
    _validate_domain(parsed_origin.netloc)

    # Sanitize path components to prevent traversal attacks
    safe_kind = _sanitize_path_component(content_kind)
    safe_id = _sanitize_path_component(content_id)

    # Build the path component (e.g. "/image/abc123")
    path = posixpath.join(parsed_origin.path, safe_kind, safe_id)

    # Reconstruct the full URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_origin.scheme,
            parsed_origin.netloc,
            path,
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return final_url

# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # These calls will succeed
    print(generate_cdn_content_url("https://cdn.example.com/", "12345", "image"))
    print(generate_cdn_content_url("https://assets.myapp.org/assets/", "logo.png", "image"))

    # This call will raise ValueError due to disallowed domain
    try:
        generate_cdn_content_url("https://evil.com/", "id", "script")
    except ValueError as exc:
        print(f"Error: {exc}")

    # This call will raise ValueError due to malicious content_id
    try:
        generate_cdn_content_url("https://cdn.example.com/", "../etc/passwd", "image")
    except ValueError as exc:
        print(f"Error: {exc}")