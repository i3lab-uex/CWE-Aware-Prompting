#!/usr/bin/env python3
"""
Utility module for constructing CDN resource URLs safely.
"""

import urllib.parse
from typing import Set

# --------------------------------------------------------------------------- #
# Configuration: list of domains that are considered safe CDNs.
# In a real application this should be read from configuration or environment
# and kept up‑to‑date with the actual CDN providers in use.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.securecdn.net",
    "static.contentprovider.org",
}

# --------------------------------------------------------------------------- #
def create_resource_url(base_cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Build a full URL for a CDN resource.

    Parameters
    ----------
    base_cdn_url : str
        The base URL of the CDN (e.g. "https://cdn.example.com/").
    res_id : str
        The unique identifier of the resource (e.g. "logo.png").
    res_type : str
        The type/category of the resource (e.g. "image", "script").

    Returns
    -------
    str
        The fully qualified URL to the requested resource.

    Raises
    ------
    ValueError
        If the resolved URL does not resolve to an allowed CDN domain.
    """
    # Normalise inputs
    if not isinstance(base_cdn_url, str):
        raise TypeError("base_cdn_url must be a string")
    if not isinstance(res_id, str):
        raise TypeError("res_id must be a string")
    if not isinstance(res_type, str):
        raise TypeError("res_type must be a string")

    # Construct the path portion: /{res_type}/{res_id}
    # Ensure no leading/trailing slashes interfere
    path = urllib.parse.urljoin("/", f"{res_type.strip('/')}/{res_id.lstrip('/')}")
    # Join the base CDN URL with the constructed path
    full_url = urllib.parse.urljoin(base_cdn_url, path)

    # Parse the URL to extract the hostname
    parsed = urllib.parse.urlparse(full_url)
    host = parsed.hostname

    # Validate that the hostname is in the whitelist
    if host not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Disallowed CDN domain: '{host}'. Allowed domains are: {sorted(ALLOWED_CDN_DOMAINS)}"
        )

    return full_url

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage and simple test cases
    try:
        print(create_resource_url("https://cdn.example.com/", "logo.png", "image"))
        # Expected: https://cdn.example.com/image/logo.png

        # This should raise an error
        print(create_resource_url("https://malicious.com/", "evil.js", "script"))
    except Exception as e:
        print(f"Error: {e}")