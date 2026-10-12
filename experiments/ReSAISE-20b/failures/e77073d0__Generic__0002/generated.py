#!/usr/bin/env python3
"""
Utility to build a CDN resource URL from a base CDN URL, file ID and type.
"""

import re
from urllib.parse import urlparse, urlunparse, urlencode

# List of allowed CDN domains.  In a real project this would come from
# configuration or environment variables.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.prod.net",
    "static.cdn.org",
}

# Regular expression to validate the file type (alphanumeric + underscore).
_FILE_TYPE_RE = re.compile(r"^[a-zA-Z0-9_]+$")

def build_cdn_resource_url(cdn_url_base: str, file_id: str, file_type: str) -> str:
    """
    Construct a fully qualified CDN URL for the given resource.

    Parameters
    ----------
    cdn_url_base : str
        The base URL of the CDN (e.g. ``https://cdn.example.com``).
    file_id : str
        Unique identifier for the resource.
    file_type : str
        Resource type (e.g. ``image`` or ``script``).

    Returns
    -------
    str
        The full URL to the requested resource.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain that is not in
        :data:`ALLOWED_CDN_DOMAINS` or if ``file_type`` contains invalid
        characters.
    """
    # Validate file type
    if not _FILE_TYPE_RE.match(file_type):
        raise ValueError(f"Invalid file type: {file_type!r}")

    # Parse the base URL
    parsed = urlparse(cdn_url_base)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_url_base!r}")

    # Ensure the domain is allowed
    if parsed.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Unauthorized CDN domain: {parsed.hostname!r}. "
            f"Allowed domains are: {sorted(ALLOWED_CDN_DOMAINS)}"
        )

    # Build the path.  Use ``/`` as separator and ensure no double slashes.
    # e.g. /image/<file_id>
    path = f"/{file_type.rstrip('/')}/{file_id.lstrip('/')}"

    # Reconstruct the URL preserving scheme and netloc
    full_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            path,
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return full_url


# --------------------- Example usage (for manual testing) ---------------------
if __name__ == "__main__":
    try:
        url = build_cdn_resource_url(
            "https://cdn.example.com",
            "abc123def456",
            "image"
        )
        print("Constructed URL:", url)
    except ValueError as exc:
        print("Error:", exc)