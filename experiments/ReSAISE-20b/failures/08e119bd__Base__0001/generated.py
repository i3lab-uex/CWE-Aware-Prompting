#!/usr/bin/env python3
"""
Utility to generate a secure CDN resource URL.

The function validates that the resulting URL resolves to one of
the allowed CDN domains, preventing open‑redirect attacks (CWE-601).
"""

import urllib.parse
from typing import Set

# Example set of allowed CDN domains – replace with real values.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.contentprovider.org",
}

def generate_external_resource_link(
    cdn_host_url: str,
    resource_tag: str,
    resource_category: str
) -> str:
    """
    Construct a fully-qualified URL for a CDN-hosted resource.

    Parameters
    ----------
    cdn_host_url : str
        Base URL of the CDN (e.g. "https://cdn.example.com/").
    resource_tag : str
        Unique identifier of the resource (e.g. "logo.png").
    resource_category : str
        Category or sub‑directory of the resource (e.g. "image").

    Returns
    -------
    str
        The absolute URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resolved URL does not belong to an allowed CDN domain.
    """
    # Sanitize inputs
    if not isinstance(cdn_host_url, str):
        raise TypeError("cdn_host_url must be a string")
    if not isinstance(resource_tag, str):
        raise TypeError("resource_tag must be a string")
    if not isinstance(resource_category, str):
        raise TypeError("resource_category must be a string")

    # Ensure the base URL ends with a slash for correct joining
    if not cdn_host_url.endswith("/"):
        cdn_host_url += "/"

    # Quote the components to avoid path traversal or injection
    safe_category = urllib.parse.quote(resource_category.strip("/"))
    safe_tag = urllib.parse.quote(resource_tag.strip("/"))

    # Build the relative path
    relative_path = f"{safe_category}/{safe_tag}"

    # Resolve to an absolute URL
    full_url = urllib.parse.urljoin(cdn_host_url, relative_path)

    # Parse the URL to inspect its components
    parsed = urllib.parse.urlparse(full_url)
    netloc = parsed.netloc.lower()

    # Strip port if present for domain comparison
    domain = netloc.split(":")[0]

    if domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Disallowed CDN domain: {domain}. "
            f"Allowed domains are: {sorted(ALLOWED_CDN_DOMAINS)}"
        )

    return full_url

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     url = generate_external_resource_link(
#         "https://cdn.example.com",
#         "logo.png",
#         "images"
#     )
#     print(url)