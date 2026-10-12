#!/usr/bin/env python3
"""
Utility for building CDN resource URLs with strict validation.
"""

from __future__ import annotations

import re
import urllib.parse
from typing import Set

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# A set of domains that are considered trusted CDNs.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.mysite.org",
}

# Regular expression to detect potentially dangerous path components.
_DANGEROUS_PATH_RE = re.compile(r"\.\.|\\|\/")

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_valid_domain(domain: str) -> bool:
    """
    Checks whether the given domain is in the allowed list.
    """
    return domain.lower() in ALLOWED_CDN_DOMAINS


def _sanitize_path_component(component: str) -> str:
    """
    Ensure that a path component does not contain traversal or escape characters.
    Raises ValueError if the component is unsafe.
    """
    if _DANGEROUS_PATH_RE.search(component):
        raise ValueError(f"Unsafe path component detected: {component!r}")
    # Normalize the component to avoid double slashes
    return urllib.parse.quote(component, safe="")

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def build_cdn_resource_url(
    cdn_url: str, resource_identifier: str, resource_kind: str
) -> str:
    """
    Build a fully-qualified CDN URL for a given resource.

    Parameters
    ----------
    cdn_url : str
        Base CDN URL (e.g., "https://cdn.example.com").
    resource_identifier : str
        Unique identifier for the resource (e.g., "logo.png").
    resource_kind : str
        Kind of resource, typically a directory name (e.g., "image").

    Returns
    -------
    str
        The fully-qualified URL to the resource.

    Raises
    ------
    ValueError
        If the CDN domain is not allowed or if any component contains unsafe characters.
    """
    # Parse the base URL
    parsed = urllib.parse.urlparse(cdn_url)

    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    if not parsed.netloc:
        raise ValueError("CDN URL must contain a network location")

    if not _is_valid_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not an allowed CDN")

    # Sanitize path components
    kind_clean = _sanitize_path_component(resource_kind.strip("/"))
    id_clean = _sanitize_path_component(resource_identifier.strip("/"))

    # Construct the new path
    new_path_parts = [kind_clean, id_clean]
    new_path = "/".join(new_path_parts)

    # Rebuild the URL with the sanitized path
    rebuilt = parsed._replace(path=f"/{new_path}")
    final_url = urllib.parse.urlunparse(rebuilt)

    # Final safety check: ensure the resulting URL still points to an allowed domain
    final_parsed = urllib.parse.urlparse(final_url)
    if not _is_valid_domain(final_parsed.netloc):
        raise ValueError("Resulting URL points to an unauthorized domain")

    return final_url

# --------------------------------------------------------------------------- #
# Example usage (commented out for production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = build_cdn_resource_url(
            "https://cdn.example.com", "logo.png", "image"
        )
        print(url)  # https://cdn.example.com/image/logo.png
    except ValueError as exc:
        print(f"URL construction failed: {exc}")