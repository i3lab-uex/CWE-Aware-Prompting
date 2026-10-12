#!/usr/bin/env python3
"""
Utility for constructing CDN resource URLs with domain validation.
"""

from urllib.parse import urlparse, urljoin
from typing import Set

# Define a set of allowed CDN domains.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.cdn.net",
}

def create_resource_url(base_cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Build a fully-qualified CDN URL for a resource.

    Parameters
    ----------
    base_cdn_url : str
        Base CDN URL, e.g. "https://cdn.example.com/"
    res_id : str
        Unique resource identifier (e.g. a hash or filename)
    res_type : str
        Type of the resource, e.g. "image", "script"

    Returns
    -------
    str
        Fully-qualified URL for the requested resource.

    Raises
    ------
    ValueError
        If the base CDN URL is malformed or does not belong to an allowed domain.
    """
    # Parse the base URL and ensure it has a scheme
    parsed = urlparse(base_cdn_url)
    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Invalid or unsupported scheme in base URL: {base_cdn_url}")

    # Verify the domain is allowed
    hostname = parsed.hostname
    if not hostname or hostname.lower() not in {d.lower() for d in ALLOWED_CDN_DOMAINS}:
        raise ValueError(f"Domain '{hostname}' is not an allowed CDN domain")

    # Normalize the resource path
    # Ensure there are no leading/trailing slashes that could break urljoin
    res_type_clean = res_type.strip("/").lower()
    res_id_clean = res_id.strip("/")

    # Construct the relative path
    relative_path = f"{res_type_clean}/{res_id_clean}"

    # Join with the base URL
    full_url = urljoin(base_cdn_url.rstrip("/") + "/", relative_path)

    # Final sanity check: ensure the resulting URL still points to the same domain
    final_parsed = urlparse(full_url)
    if final_parsed.hostname.lower() != hostname.lower():
        raise ValueError("Constructed URL points to a different domain")

    return full_url