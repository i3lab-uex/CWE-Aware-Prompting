#!/usr/bin/env python3
"""
Utility to build a CDN resource URL with domain validation.
"""

import urllib.parse

# Example set of allowed CDN domains – adjust as needed for your environment
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net",
}

def create_resource_url(base_cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Construct a fully‑qualified URL for a resource hosted on a CDN.

    Parameters
    ----------
    base_cdn_url : str
        Base URL of the CDN (must include scheme, e.g. https://cdn.example.com).
    res_id : str
        Unique identifier for the requested resource.
    res_type : str
        Type of resource, e.g. "image", "script", etc.

    Returns
    -------
    str
        Fully resolved URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the base URL is malformed or its domain is not in ALLOWED_CDN_DOMAINS.
    """
    # Parse the base URL
    parsed = urllib.parse.urlparse(base_cdn_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Base CDN URL must include scheme and host: {base_cdn_url!r}")

    # Normalise domain (strip port if present)
    host = parsed.hostname
    if host is None:
        raise ValueError(f"Unable to determine hostname from URL: {base_cdn_url!r}")

    if host not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{host}' is not an allowed CDN domain")

    # Build the path component
    # Ensure res_type and res_id are safe for URLs by percent‑encoding them
    path = urllib.parse.urljoin(
        parsed.path.rstrip("/") + "/",
        f"{urllib.parse.quote(res_type)}/{urllib.parse.quote(res_id)}"
    )

    # Reconstruct the full URL
    new_parsed = parsed._replace(path=path, query="", fragment="")
    return urllib.parse.urlunparse(new_parsed)

# Example usage (commented out – remove to test)
# if __name__ == "__main__":
#     url = create_resource_url("https://cdn.example.com/assets", "logo.png", "image")
#     print(url)