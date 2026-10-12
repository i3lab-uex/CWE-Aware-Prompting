#!/usr/bin/env python3
"""
Utility to construct a secure CDN resource URL.
"""

from urllib.parse import urlparse, urljoin

# Set of domains that are considered safe CDN hosts.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "static.example.org",
    "assets.myapp.net",
}

def build_cdn_resource_url(cdn_url: str, resource_identifier: str, resource_kind: str) -> str:
    """
    Construct a full URL to a CDN-hosted resource.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN (e.g. "https://cdn.example.com/").
    resource_identifier : str
        Unique identifier for the resource (e.g. a hash or filename).
    resource_kind : str
        Kind of resource, e.g. "image" or "script".

    Returns
    -------
    str
        The fully-qualified URL to the requested resource.

    Raises
    ------
    ValueError
        If the constructed URL is not under an allowed CDN domain.
    """
    # Normalize and validate the base CDN URL
    parsed_base = urlparse(cdn_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_url!r}")

    # Ensure the domain is allowed
    if parsed_base.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain {parsed_base.hostname!r} is not an allowed CDN host")

    # Build the resource path
    # Use posixpath to avoid accidental double slashes
    from pathlib import PurePosixPath

    resource_path = str(PurePosixPath(parsed_base.path) / resource_kind / resource_identifier)

    # Construct the final URL
    final_url = urljoin(f"{parsed_base.scheme}://{parsed_base.netloc}", resource_path)

    # Final check: ensure the resulting URL still uses an allowed domain
    final_parsed = urlparse(final_url)
    if final_parsed.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Resulting URL {final_url!r} points to disallowed domain")

    return final_url

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(build_cdn_resource_url(
#         "https://cdn.example.com/",
#         "abc123def456",
#         "image"
#     ))