#!/usr/bin/env python3
"""
Utility for constructing CDN resource URLs with domain whitelisting.

The module validates that the resulting URL belongs to an allowed CDN domain
to prevent misuse such as open redirects or leaking sensitive data.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import urllib.parse
from typing import Final, Set


# --------------------------------------------------------------------------- #
# Configuration:  Whitelisted CDN domains.  Adjust as needed for your setup.
# --------------------------------------------------------------------------- #
ALLOWED_CDN_DOMAINS: Final[Set[str]] = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.anotherdomain.org",
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def generate_external_resource_link(
    cdn_host_url: str,
    resource_tag: str,
    resource_category: str,
) -> str:
    """
    Build a full CDN URL for the specified resource.

    Parameters
    ----------
    cdn_host_url : str
        Base URL of the CDN (e.g. ``https://cdn.example.com``).
    resource_tag : str
        Unique identifier for the resource (e.g. ``logo.png``).
    resource_category : str
        Category of the resource, e.g. ``image``, ``script``.

    Returns
    -------
    str
        A fully qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the constructed URL does not resolve to a domain in
        :data:`ALLOWED_CDN_DOMAINS`.

    Notes
    -----
    * The function normalises the path to avoid duplicate slashes.
    * Only the hostname is checked against :data:`ALLOWED_CDN_DOMAINS`; the
      scheme is preserved from ``cdn_host_url``.
    """
    if not cdn_host_url:
        raise ValueError("The CDN host URL must not be empty.")
    if not resource_tag:
        raise ValueError("Resource tag must not be empty.")
    if not resource_category:
        raise ValueError("Resource category must not be empty.")

    # Parse the base URL and enforce a scheme.
    parsed_base = urllib.parse.urlparse(cdn_host_url)
    if not parsed_base.scheme:
        raise ValueError("CDN host URL must include a scheme (e.g., https://).")

    # Build the path component: /<category>/<tag>
    normalized_path = urllib.parse.urljoin(
        f"/{resource_category.rstrip('/')}/", resource_tag.lstrip("/")
    )

    # Construct the full URL
    full_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            normalized_path,
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    # Verify that the hostname is allowed
    host = urllib.parse.urlparse(full_url).hostname or ""
    if host not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Disallowed CDN domain: {host}. Allowed domains are "
            f"{', '.join(sorted(ALLOWED_CDN_DOMAINS))}"
        )

    return full_url


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        url = generate_external_resource_link(
            "https://cdn.example.com",
            "logo.png",
            "image"
        )
        print("Generated URL:", url)
    except ValueError as exc:
        print("Error:", exc)