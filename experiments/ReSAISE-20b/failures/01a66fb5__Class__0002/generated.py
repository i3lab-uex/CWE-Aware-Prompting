#!/usr/bin/env python3
"""
Utility to construct CDN resource URLs with strict domain validation.
"""

from urllib.parse import urlparse, urljoin
from typing import Set

# Define a set of allowed CDN domains. In practice this would be populated
# from configuration or environment variables.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.mysite.org",
}

def create_cdn_resource_link(
    cdn_url_base: str,
    resource_identifier: str,
    type_of_resource: str
) -> str:
    """
    Construct a full URL to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url_base : str
        The base URL of the CDN, e.g. "https://cdn.example.com/"
    resource_identifier : str
        Identifier of the requested resource, e.g. "logo.png"
    type_of_resource : str
        Type of the resource (e.g., 'image', 'script').  Used only for logging
        or future extensions; not part of the URL.

    Returns
    -------
    str
        The fully qualified, validated URL.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain not in :data:`ALLOWED_CDN_DOMAINS`.
    """
    # Ensure base URL ends with a slash to avoid path concatenation issues.
    if not cdn_url_base.endswith("/"):
        base = f"{cdn_url_base}/"
    else:
        base = cdn_url_base

    # Join the base with the resource identifier.
    raw_url = urljoin(base, resource_identifier)

    # Parse to extract netloc (domain + optional port).
    parsed = urlparse(raw_url)
    domain = parsed.hostname

    if domain is None:
        raise ValueError(f"Malformed URL produced: {raw_url}")

    # Validate against allowed domains.
    if domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Disallowed CDN domain '{domain}'. Allowed domains: {sorted(ALLOWED_CDN_DOMAINS)}"
        )

    # Optionally enforce HTTPS for security.
    if parsed.scheme != "https":
        raise ValueError(
            f"URL scheme must be HTTPS, got '{parsed.scheme}'. URL: {raw_url}"
        )

    return raw_url

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    try:
        url = create_cdn_resource_link(
            "https://cdn.example.com",
            "images/logo.png",
            "image"
        )
        print(f"Generated CDN URL: {url}")
    except ValueError as e:
        print(f"Error: {e}")