#!/usr/bin/env python3
"""
Utility to generate a fully‑qualified URL for an external resource hosted on a CDN.

The function validates that the resulting URL resolves to one of the
pre‑approved CDN domains.  This protects against CWE‑610 (Externally
Controlled Reference to a Resource in Another Sphere) by ensuring that
the resource URL cannot be forged to point at an arbitrary domain.
"""

from __future__ import annotations

import urllib.parse
from typing import Final, Set

# ----------------------------------------------------------------------
# Configuration: allowed CDN domains.
# ----------------------------------------------------------------------
ALLOWED_CDN_DOMAINS: Final[Set[str]] = {
    "cdn.example.com",
    "assets.safe-cdn.org",
    "static.myapp.net",
}

# ----------------------------------------------------------------------
# Main helper
# ----------------------------------------------------------------------
def generate_external_resource_link(
    cdn_host_url: str,
    resource_tag: str,
    resource_category: str,
) -> str:
    """
    Build a URL for an external resource on a CDN.

    Parameters
    ----------
    cdn_host_url : str
        Base URL of the CDN (e.g., "https://cdn.example.com").
    resource_tag : str
        Unique identifier of the resource (e.g., "logo.png").
    resource_category : str
        Category type, used as a sub‑path (e.g., "image", "script").

    Returns
    -------
    str
        The fully qualified URL for the resource.

    Raises
    ------
    ValueError
        If the constructed URL does not resolve to an allowed CDN domain.
    """
    # 1. Sanitize inputs: strip whitespace, ensure strings
    if not all(isinstance(arg, str) for arg in (cdn_host_url, resource_tag, resource_category)):
        raise TypeError("All arguments must be strings")

    cdn_host_url = cdn_host_url.strip()
    resource_tag = resource_tag.strip().lstrip("/")
    resource_category = resource_category.strip().lstrip("/")

    # 2. Parse the base CDN URL
    parsed_cdn = urllib.parse.urlparse(cdn_host_url)
    if not parsed_cdn.scheme or not parsed_cdn.netloc:
        raise ValueError(f"Invalid CDN host URL: {cdn_host_url!r}")

    # 3. Build the path: /{category}/{tag}
    new_path = urllib.parse.urljoin(parsed_cdn.path + "/", f"{resource_category}/{resource_tag}")

    # 4. Reconstruct the full URL
    constructed_url = urllib.parse.urlunparse(
        (
            parsed_cdn.scheme,
            parsed_cdn.netloc,
            new_path,
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    # 5. Validate the domain against allowed CDNs
    if parsed_cdn.netloc.lower() not in {d.lower() for d in ALLOWED_CDN_DOMAINS}:
        raise ValueError(
            f"Disallowed CDN domain: {parsed_cdn.netloc!r}. "
            f"Allowed domains are: {', '.join(sorted(ALLOWED_CDN_DOMAINS))}"
        )

    return constructed_url


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        url = generate_external_resource_link(
            cdn_host_url="https://cdn.example.com",
            resource_tag="logo.png",
            resource_category="image"
        )
        print("Generated URL:", url)
    except Exception as e:
        print("Error:", e)