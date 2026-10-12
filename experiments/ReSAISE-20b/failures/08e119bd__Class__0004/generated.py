#!/usr/bin/env python3
"""
Utility to generate a fully‑qualified URL for an external resource hosted on a CDN.

The function validates that the resulting URL belongs to one of the pre‑approved
CDN domains.  It also performs basic sanitisation of user supplied values to
mitigate the risk of CWE‑610 – Externally Controlled Reference to a Resource in
Another Sphere.
"""

from __future__ import annotations

import urllib.parse
from typing import Set

# --------------------------------------------------------------------------- #
# Configuration – only these domains are considered safe for CDNs.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.safedomain.org",
    "static.myapp.net",
}

# --------------------------------------------------------------------------- #
def generate_external_resource_link(
    cdn_host_url: str,
    resource_tag: str,
    resource_category: str,
) -> str:
    """
    Construct a CDN URL for the given resource.

    Parameters
    ----------
    cdn_host_url : str
        Base URL of the CDN, e.g. "https://cdn.example.com/"
    resource_tag : str
        Unique identifier for the resource (e.g. a filename or hash).
    resource_category : str
        Category of the resource, such as "image" or "script".

    Returns
    -------
    str
        Fully resolved URL pointing to the resource on the CDN.

    Raises
    ------
    ValueError
        If the final URL does not resolve to an allowed CDN domain.
    """
    # Normalise the base URL – ensure it ends with a slash so that urljoin
    # behaves predictably.
    if not cdn_host_url.endswith("/"):
        base = f"{cdn_host_url}/"
    else:
        base = cdn_host_url

    # Sanitize the category – only allow alphanumerics to avoid directory traversal.
    if not resource_category.isalnum():
        raise ValueError("resource_category must be alphanumeric")

    # Encode the tag to safely embed it in a URL path component.
    safe_tag = urllib.parse.quote(resource_tag, safe="")

    # Build the relative path: <category>/<tag>
    rel_path = f"{resource_category}/{safe_tag}"

    # Resolve the full URL.
    full_url = urllib.parse.urljoin(base, rel_path)

    # Parse the resulting URL to inspect its domain.
    parsed = urllib.parse.urlparse(full_url)
    netloc = parsed.netloc.lower()

    # The domain may contain a port; strip it for comparison.
    host = netloc.split(":")[0]

    if host not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"URL domain '{host}' is not an allowed CDN")

    return full_url


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage
    try:
        url = generate_external_resource_link(
            "https://cdn.example.com",
            "logo.svg",
            "image"
        )
        print(url)
    except ValueError as exc:
        print(f"Invalid URL: {exc}")