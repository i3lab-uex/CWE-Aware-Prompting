#!/usr/bin/env python3
"""
Utility to construct a secure URL for external resources served from a CDN.

The function validates that the final URL resolves to an allowed CDN domain
to prevent open redirect or SSRF attacks.
"""

from urllib.parse import urljoin, urlparse
from typing import Set

# Define the set of allowed CDN domains (example entries)
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net",
}

def construct_external_resource_url(
    cdn_base_url: str,
    resource_id: str,
    resource_type: str
) -> str:
    """
    Construct a fully-qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base_url : str
        Base URL of the CDN (e.g., "https://cdn.example.com/").
    resource_id : str
        Identifier of the specific resource (e.g., "logo.png" or "app.js").
    resource_type : str
        Type/category of the resource (e.g., "image", "script").

    Returns
    -------
    str
        Fully-qualified URL pointing to the resource on the CDN.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to an allowed CDN domain.
    """
    if not cdn_base_url:
        raise ValueError("cdn_base_url must be a non-empty string")

    if not resource_id:
        raise ValueError("resource_id must be a non-empty string")

    if not resource_type:
        raise ValueError("resource_type must be a non-empty string")

    # Normalise base URL to ensure it ends with a slash
    normalized_base = cdn_base_url if cdn_base_url.endswith("/") else cdn_base_url + "/"

    # Build the path: /{resource_type}/{resource_id}
    relative_path = f"{resource_type.rstrip('/')}/{resource_id.lstrip('/')}"

    # Combine base and relative path
    full_url = urljoin(normalized_base, relative_path)

    # Parse the URL to extract the domain
    parsed = urlparse(full_url)
    netloc = parsed.netloc

    # Strip port if present for domain comparison
    domain = netloc.split(":")[0]

    if domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Disallowed CDN domain: '{domain}'. Allowed domains are: "
            f"{', '.join(sorted(ALLOWED_CDN_DOMAINS))}"
        )

    return full_url

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     url = construct_external_resource_url(
#         cdn_base_url="https://cdn.example.com",
#         resource_id="images/logo.png",
#         resource_type="image"
#     )
#     print(url)