#!/usr/bin/env python3
"""
Utility to build a secure CDN resource URL.

The function ensures that the constructed URL resolves to one of the
predefined allowed CDN domains, preventing accidental or malicious
redirects (CWE‑610).
"""

from urllib.parse import urlparse, urljoin, quote
from typing import Set

# --------------------------------------------------------------------------- #
# Predefined set of CDN domains that are considered safe.
# In a real application this should be configured via environment
# variables or a secure configuration file.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.example.org",
    # Add other trusted CDN domains here
}
# --------------------------------------------------------------------------- #

def create_cdn_resource_link(
    cdn_url_base: str,
    resource_identifier: str,
    type_of_resource: str
) -> str:
    """
    Construct a fully-qualified URL to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN (e.g. "https://cdn.example.com").
    resource_identifier : str
        Identifier of the requested resource (e.g. "logo.png").
    type_of_resource : str
        Type of the resource, used to build a logical path (e.g.
        "image", "script").

    Returns
    -------
    str
        The fully constructed URL.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to an allowed CDN domain.
    """
    # Sanity check for empty inputs
    if not cdn_url_base or not resource_identifier or not type_of_resource:
        raise ValueError("All arguments must be non-empty strings")

    # Ensure the base URL is well-formed
    parsed_base = urlparse(cdn_url_base)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_url_base}")

    # Verify that the domain is in the allowed list
    if parsed_base.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Domain '{parsed_base.hostname}' is not an allowed CDN domain"
        )

    # Construct the resource path safely
    # Use quote to escape any unsafe characters in identifiers
    safe_identifier = quote(resource_identifier, safe='')
    resource_path = f"/{type_of_resource.rstrip('/')}/{safe_identifier}"

    # Combine the base URL with the resource path
    full_url = urljoin(cdn_url_base.rstrip('/') + '/', resource_path.lstrip('/'))

    # Final verification: the resolved URL must still target an allowed domain
    final_parsed = urlparse(full_url)
    if final_parsed.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Constructed URL resolves to disallowed domain '{final_parsed.hostname}'"
        )

    return full_url