#!/usr/bin/env python3
"""
Utility for building and validating external CDN resource URLs.

The function `create_external_resource_link` constructs a URL that points to a
resource on an external CDN.  It verifies that the resulting host is part of a
whitelist (`ALLOWED_CDN_DOMAINS`) to mitigate CWE‑601 (Open Redirect).

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import urllib.parse
from typing import Iterable, Set


# --------------------------------------------------------------------------- #
# Configuration: allowed CDN domains.  In a real project this would probably
# come from environment variables or a configuration file.
# --------------------------------------------------------------------------- #
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net",
}


def _normalize_domain(domain: str) -> str:
    """
    Normalise a domain name for comparison.
    Removes leading/trailing whitespace and lower‑cases the host.
    """
    return domain.strip().lower()


def create_external_resource_link(cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Assemble a fully‑qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN (e.g. "https://cdn.example.com").
    res_id : str
        Unique identifier for the resource (e.g. "12345").
    res_type : str
        Type/category of the resource (e.g. "image", "script").

    Returns
    -------
    str
        A validated URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a host that is not in
        :data:`ALLOWED_CDN_DOMAINS`.
    """
    # Ensure all inputs are strings
    if not isinstance(cdn_url, str):
        raise TypeError("cdn_url must be a string")
    if not isinstance(res_id, str):
        raise TypeError("res_id must be a string")
    if not isinstance(res_type, str):
        raise TypeError("res_type must be a string")

    # Build the path: /{res_type}/{res_id}
    path = urllib.parse.urljoin("/", f"{res_type.rstrip('/')}/")
    full_path = urllib.parse.urljoin(path, res_id.lstrip("/"))

    # Construct the absolute URL
    joined_url = urllib.parse.urljoin(cdn_url.rstrip("/") + "/", full_path)

    # Parse the resulting URL to extract host information
    parsed = urllib.parse.urlparse(joined_url)

    # Reject URLs without a scheme or host
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {joined_url}")

    # Validate the host against the whitelist
    host = _normalize_domain(parsed.netloc.split(":")[0])  # ignore port if present
    if host not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Unauthorized CDN domain: {host}")

    # Return the fully constructed and validated URL
    return joined_url


# --------------------------------------------------------------------------- #
# Example usage (for testing / demonstration only)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        url = create_external_resource_link(
            cdn_url="https://cdn.example.com",
            res_id="images/hero.png",
            res_type="image"
        )
        print("Generated URL:", url)
    except Exception as exc:
        print("Error:", exc)