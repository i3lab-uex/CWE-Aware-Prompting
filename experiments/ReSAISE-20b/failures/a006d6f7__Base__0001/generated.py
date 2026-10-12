#!/usr/bin/env python3
"""
Utility for safely generating CDN URLs.

The function ensures that the final URL resolves to one of the
approved CDN domains and rejects any attempt to redirect to an
unauthorized domain, protecting against CWE‑601 (Open Redirect).
"""

from urllib.parse import urljoin, urlparse
from typing import Iterable

# Allowed CDN domains – add your trusted CDN hosts here.
ALLOWED_CDN_DOMAINS: Iterable[str] = (
    "cdn.example.com",
    "assets.myapp.net",
)

def generate_cdn_content_url(
    cdn_origin_url: str,
    content_id: str,
    content_kind: str
) -> str:
    """
    Construct a fully-qualified CDN URL for the requested content.

    Parameters
    ----------
    cdn_origin_url : str
        The base URL of the CDN (e.g. "https://cdn.example.com/").
    content_id : str
        Unique identifier for the resource.
    content_kind : str
        Type of resource, e.g. "image" or "script".

    Returns
    -------
    str
        A validated absolute URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resolved URL does not point to an allowed CDN domain.
    """
    # Sanitize inputs: strip whitespace and enforce string type
    cdn_origin_url = str(cdn_origin_url).strip()
    content_id = str(content_id).strip()
    content_kind = str(content_kind).strip()

    if not cdn_origin_url:
        raise ValueError("cdn_origin_url must be a non-empty string")

    # Ensure the origin URL has a scheme; default to https if missing
    parsed_origin = urlparse(cdn_origin_url)
    if not parsed_origin.scheme:
        cdn_origin_url = f"https://{cdn_origin_url}"
        parsed_origin = urlparse(cdn_origin_url)

    # Build the relative path for the resource
    # e.g., "/image/abc123"
    resource_path = f"/{content_kind}/{content_id}"

    # Construct the absolute URL
    final_url = urljoin(cdn_origin_url, resource_path)

    # Validate that the resolved URL points to an allowed CDN domain
    final_parsed = urlparse(final_url)
    if final_parsed.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"URL resolves to unauthorized domain: {final_parsed.netloc}"
        )

    return final_url


# Example usage (remove or guard with __name__ == "__main__" in production)
if __name__ == "__main__":
    try:
        url = generate_cdn_content_url(
            "https://cdn.example.com",
            "abc123",
            "image"
        )
        print(url)  # https://cdn.example.com/image/abc123
    except ValueError as exc:
        print(f"Invalid CDN URL: {exc}")