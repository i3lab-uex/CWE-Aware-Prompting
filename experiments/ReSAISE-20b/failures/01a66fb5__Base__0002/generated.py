#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utility to construct a CDN resource URL safely.
"""

from urllib.parse import urlparse, urljoin
import posixpath

# Example set of allowed CDN domains. In a real application this would be
# defined elsewhere and imported from a configuration module.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net",
}

def create_cdn_resource_link(cdn_url_base: str,
                             resource_identifier: str,
                             type_of_resource: str) -> str:
    """
    Build a fully-qualified URL pointing to an external resource hosted on
    a known CDN.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN (e.g. "https://cdn.example.com/").
    resource_identifier : str
        Identifier of the desired resource.  It may contain sub‑paths but
        must not include protocol or domain.
    type_of_resource : str
        Type of resource (e.g. "image", "script").  This value is not used
        for validation but can be appended to the path if desired.

    Returns
    -------
    str
        The fully constructed URL that points to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in
        ``ALLOWED_CDN_DOMAINS``.
    """

    # Sanitize the resource identifier:
    # - Remove leading slashes to avoid absolute paths.
    # - Normalize path components (e.g. "./", "../") to prevent
    #   traversal outside the intended CDN root.
    clean_identifier = posixpath.normpath(resource_identifier.lstrip("/"))

    # Construct the URL relative to the CDN base.
    # urljoin handles trailing slashes correctly.
    tentative_url = urljoin(cdn_url_base.rstrip("/") + "/", clean_identifier)

    # Optionally, append a type-specific subdirectory or query.
    if type_of_resource:
        tentative_url = urljoin(tentative_url.rstrip("/") + "/", type_of_resource)

    # Parse the resulting URL to extract the network location.
    parsed = urlparse(tentative_url)

    # Ensure the scheme is HTTPS to avoid downgrade attacks.
    if parsed.scheme.lower() != "https":
        raise ValueError(f"URL scheme must be HTTPS, got '{parsed.scheme}'")

    # Verify the hostname is one of the allowed CDN domains.
    if parsed.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {parsed.hostname!r}")

    # Return the fully constructed URL as a string.
    return tentative_url


# --------------------------------------------------------------------------- #
# Example usage (would normally be in tests or application code):
if __name__ == "__main__":
    try:
        url = create_cdn_resource_link(
            cdn_url_base="https://cdn.example.com/",
            resource_identifier="/images/logo.png",
            type_of_resource="image"
        )
        print(f"Generated CDN URL: {url}")
    except ValueError as exc:
        print(f"Failed to generate CDN URL: {exc}")