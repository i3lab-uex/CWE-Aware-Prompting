#!/usr/bin/env python3
"""
Utility for generating CDN resource URLs with domain whitelisting.
"""

from urllib.parse import urljoin, urlparse
from typing import Set

# --------------------------------------------------------------------------- #
# Example set of allowed CDN domains. In a real application this would be
# configured elsewhere (e.g., via environment variables or a config file).
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net",
}

# --------------------------------------------------------------------------- #
def create_cdn_resource_link(
    cdn_url_base: str,
    resource_identifier: str,
    type_of_resource: str
) -> str:
    """
    Construct a fully qualified CDN URL for the requested resource.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN (e.g., "https://cdn.example.com/").
    resource_identifier : str
        Path or identifier for the specific resource.
    type_of_resource : str
        Resource type (e.g., "image", "script"). This is used only for
        documentation purposes and does not affect the URL generation.

    Returns
    -------
    str
        The fully resolved CDN URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in
        ``ALLOWED_CDN_DOMAINS``.
    """

    # Ensure the base ends with a slash so urljoin behaves predictably
    if not cdn_url_base.endswith("/"):
        base = f"{cdn_url_base}/"
    else:
        base = cdn_url_base

    # Normalise the resource identifier (strip leading slashes)
    path = resource_identifier.lstrip("/")

    # Build the URL
    full_url = urljoin(base, path)

    # Parse out the domain for validation
    parsed = urlparse(full_url)
    host = parsed.hostname

    if host is None:
        raise ValueError(f"Unable to determine hostname from URL: {full_url}")

    # Perform a simple whitelist check
    if host not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Disallowed CDN domain '{host}'. Allowed domains: {sorted(ALLOWED_CDN_DOMAINS)}"
        )

    return full_url

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Simple test harness
    try:
        url = create_cdn_resource_link(
            "https://cdn.example.com",
            "/images/logo.png",
            "image"
        )
        print(f"Generated URL: {url}")
    except ValueError as exc:
        print(f"Error: {exc}")