#!/usr/bin/env python3
"""
Utility to construct a CDN resource URL with domain validation.
"""

from urllib.parse import urlparse, urljoin
from typing import Set

# Predefined set of allowed CDN domains.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.mysite.org",
    "static.otherdomain.net",
}

def create_resource_url(base_cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Build a fully-qualified URL for a CDN-hosted resource.

    Parameters
    ----------
    base_cdn_url : str
        Base URL of the CDN (e.g., "https://cdn.example.com/").
    res_id : str
        Unique identifier of the resource (e.g., "logo.png").
    res_type : str
        Type/category of the resource (e.g., "image", "script").

    Returns
    -------
    str
        Fully-qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in :data:`ALLOWED_CDN_DOMAINS`.
    """
    # Normalise the base URL: ensure it ends with a slash for urljoin.
    if not base_cdn_url.endswith("/"):
        base_cdn_url += "/"

    # Construct the relative path.
    rel_path = f"{res_type.rstrip('/')}/{res_id.lstrip('/')}"

    # Combine into a full URL.
    full_url = urljoin(base_cdn_url, rel_path)

    # Validate the domain.
    parsed = urlparse(full_url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    if parsed.netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{parsed.netloc}' is not an allowed CDN domain.")

    return full_url