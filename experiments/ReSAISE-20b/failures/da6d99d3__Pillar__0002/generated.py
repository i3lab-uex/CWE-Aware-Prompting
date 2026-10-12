#!/usr/bin/env python3
"""
Utility for constructing secure URLs to external resources hosted on approved CDNs.
"""

from urllib.parse import urlparse, urljoin
from typing import Set

# Example set of allowed CDN domains. In a real application this should be
# populated from configuration or environment variables.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.example.org",
    "static.myapp.net",
}

def build_external_resource_link(cdn_url: str, resource_key: str, res_category: str) -> str:
    """
    Build a fully-qualified URL for an external resource, ensuring that the
    target domain is in :data:`ALLOWED_CDN_DOMAINS`.

    Parameters:
        cdn_url (str): Base URL of the CDN. May include scheme, host and optional
                       path component.
        resource_key (str): Identifier of the resource (e.g., a filename or
                            hash).
        res_category (str): Resource type/category such as 'image' or 'script'.

    Returns:
        str: The fully constructed URL.

    Raises:
        ValueError: If the resulting URL does not target an allowed CDN domain.
    """
    # Normalise base CDN URL and ensure it ends with a slash so that
    # urljoin behaves predictably.
    base = cdn_url.rstrip("/") + "/"

    # Construct the relative path: <category>/<resource_key>
    rel_path = f"{res_category.strip('/')}/{resource_key.lstrip('/')}"

    # Build the absolute URL
    full_url = urljoin(base, rel_path)

    # Parse out the hostname for validation
    parsed = urlparse(full_url)
    host = parsed.hostname or ""

    # Verify that the hostname is in the allowed list.
    if host not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Disallowed CDN domain '{host}'. Allowed domains are: "
            f"{', '.join(sorted(ALLOWED_CDN_DOMAINS))}"
        )

    return full_url

# Example usage (would normally be in a separate test module)
if __name__ == "__main__":
    try:
        url = build_external_resource_link(
            cdn_url="https://cdn.example.com/assets",
            resource_key="logo.png",
            res_category="images"
        )
        print("Generated URL:", url)
    except ValueError as e:
        print("Error:", e)