#!/usr/bin/env python3
"""
Utility for safely constructing CDN resource URLs.

The function ensures that the final URL points to a domain that is
explicitly allowed.  It uses urllib.parse for robust URL handling and
prevents directory traversal or other manipulation attacks.
"""

from __future__ import annotations

import urllib.parse
from typing import Final, Set

# Define a set of domains that are considered safe to use.
ALLOWED_CDN_DOMAINS: Final[Set[str]] = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.someprovider.net",
}


def create_cdn_resource_link(
    cdn_url_base: str,
    resource_identifier: str,
    type_of_resource: str,
) -> str:
    """
    Construct a fully-qualified CDN URL for the requested resource.

    Parameters
    ----------
    cdn_url_base : str
        The base URL of the CDN, e.g. "https://cdn.example.com".
    resource_identifier : str
        The relative path or identifier for the resource, e.g.
        "images/logo.png".
    type_of_resource : str
        The type of resource (e.g. 'image', 'script').  This is used only
        for validation and can be ignored in the URL construction.

    Returns
    -------
    str
        The fully qualified URL pointing to the resource.

    Raises
    ------
    ValueError
        If the final URL resolves to a domain not in ALLOWED_CDN_DOMAINS.
    """
    # Sanity checks on inputs
    if not cdn_url_base or not isinstance(cdn_url_base, str):
        raise ValueError("cdn_url_base must be a non-empty string")
    if not resource_identifier or not isinstance(resource_identifier, str):
        raise ValueError("resource_identifier must be a non-empty string")
    if not type_of_resource or not isinstance(type_of_resource, str):
        raise ValueError("type_of_resource must be a non-empty string")

    # Normalize the base URL
    parsed_base = urllib.parse.urlparse(cdn_url_base)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("cdn_url_base must be a valid absolute URL")

    # Ensure the base domain is allowed
    if parsed_base.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Domain '{parsed_base.netloc}' is not in the list of allowed CDN domains"
        )

    # Prevent path traversal by normalizing the resource identifier
    # Remove any leading slashes and collapse '.' and '..' segments.
    cleaned_resource = urllib.parse.urljoin("/", resource_identifier)
    # urljoin with a leading slash removes the base path, giving us a clean relative path
    cleaned_resource = urllib.parse.urlparse(cleaned_resource).path

    # Build the final URL
    final_url = urllib.parse.urljoin(cdn_url_base.rstrip("/") + "/", cleaned_resource)

    # Final check: ensure the resulting domain is still allowed
    final_parsed = urllib.parse.urlparse(final_url)
    if final_parsed.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Resulting URL domain '{final_parsed.netloc}' is not allowed"
        )

    return final_url