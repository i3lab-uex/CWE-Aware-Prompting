#!/usr/bin/env python3
"""
Utility to construct a safe CDN URL for external resources.
"""

import urllib.parse
from typing import Set

# Allowed CDN domains (example values)
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.safecdn.net",
}

def construct_external_resource_url(
    cdn_base_url: str,
    resource_id: str,
    resource_type: str
) -> str:
    """
    Construct a full URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base_url : str
        Base URL of the CDN (e.g., "https://cdn.example.com/").
    resource_id : str
        Identifier of the specific resource (e.g., "12345").
    resource_type : str
        Type/category of the resource, used to build a path segment
        (e.g., "image", "script").

    Returns
    -------
    str
        Fully-qualified, validated URL pointing to the resource.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to an allowed CDN domain.
    """
    # Parse the base URL and ensure it has a scheme
    parsed_base = urllib.parse.urlparse(cdn_base_url)
    if not parsed_base.scheme:
        raise ValueError("cdn_base_url must include a scheme (http/https).")

    # Normalise the path: ensure it ends with '/'
    base_path = parsed_base.path
    if not base_path.endswith("/"):
        base_path += "/"

    # Build the relative path for the resource
    # Example: /images/<resource_id>.jpg or /scripts/<resource_id>.js
    safe_resource_type = urllib.parse.quote_plus(resource_type.strip())
    safe_resource_id = urllib.parse.quote_plus(resource_id.strip())

    relative_path = f"{safe_resource_type}/{safe_resource_id}"

    # Join base and relative paths
    full_url = urllib.parse.urljoin(
        f"{parsed_base.scheme}://{parsed_base.netloc}{base_path}",
        relative_path,
    )

    # Validate the final domain against allowed list
    final_parsed = urllib.parse.urlparse(full_url)
    if final_parsed.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Disallowed CDN domain: {final_parsed.netloc}. "
            f"Allowed domains are: {', '.join(sorted(ALLOWED_CDN_DOMAINS))}"
        )

    return full_url

# Example usage (commented out to avoid execution during import)
if __name__ == "__main__":
    try:
        url = construct_external_resource_url(
            cdn_base_url="https://cdn.example.com/",
            resource_id="logo.png",
            resource_type="image"
        )
        print(url)  # https://cdn.example.com/image/logo.png
    except ValueError as e:
        print(f"Error: {e}")