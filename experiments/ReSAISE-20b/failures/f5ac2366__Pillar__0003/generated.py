#!/usr/bin/env python3
"""
Utility for constructing a safe URL to an external CDN resource.

The function validates that the final URL points to one of the
pre‑approved CDN domains and safely combines the base URL,
resource type, and resource identifier.
"""

from __future__ import annotations

import urllib.parse
import posixpath
from typing import Final, Set


# --------------------------------------------------------------------------- #
#  Configuration: allowed CDN domains (add real values here)
# --------------------------------------------------------------------------- #
ALLOWED_CDN_DOMAINS: Final[Set[str]] = {
    "cdn.example.com",
    "assets.myapp.net",
    # Add more trusted domains as needed
}


def _is_allowed_domain(netloc: str) -> bool:
    """
    Check whether the given netloc (host[:port]) belongs to an allowed domain.
    The port is ignored for the check.
    """
    host = netloc.split(":")[0].lower()
    return host in ALLOWED_CDN_DOMAINS


def construct_external_resource_url(
    cdn_base_url: str,
    resource_id: str,
    resource_type: str,
) -> str:
    """
    Construct a fully qualified URL for an external CDN resource.

    Parameters
    ----------
    cdn_base_url : str
        Base URL of the CDN (e.g. "https://cdn.example.com/").
    resource_id : str
        Identifier of the specific resource (e.g. "12345.png").
    resource_type : str
        Type of the resource, used as a path segment (e.g. "image", "script").

    Returns
    -------
    str
        The complete URL that points to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to an allowed CDN domain.
    """

    # Normalise and parse the base URL
    parsed_base = urllib.parse.urlparse(cdn_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_base_url!r}")

    # Validate the domain early
    if not _is_allowed_domain(parsed_base.netloc):
        raise ValueError(f"Domain {parsed_base.netloc!r} is not in the allowed CDN domains")

    # Safely encode path components
    safe_type = urllib.parse.quote(resource_type, safe="")
    safe_id = urllib.parse.quote(resource_id, safe="")

    # Join path segments using POSIX semantics to avoid double slashes
    resource_path = posixpath.join(parsed_base.path, safe_type, safe_id)

    # Build the final URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            resource_path,
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    # Final domain check (in case the path manipulation changed netloc)
    if not _is_allowed_domain(urllib.parse.urlparse(final_url).netloc):
        raise ValueError(f"Resulting URL points to an untrusted domain: {final_url!r}")

    return final_url


# --------------------------------------------------------------------------- #
#  Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        url = construct_external_resource_url(
            "https://cdn.example.com/",
            "images/photo.png",
            "image"
        )
        print("Constructed URL:", url)
    except ValueError as exc:
        print("Error:", exc)