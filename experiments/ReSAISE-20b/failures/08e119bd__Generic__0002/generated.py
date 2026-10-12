#!/usr/bin/env python3
"""
Utility to build secure CDN resource URLs.
"""

import urllib.parse

# ----------------------------------------------------------------------
# Configuration: allowed CDN domains. Add or remove entries as needed.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.provider.org",
}

# ----------------------------------------------------------------------
def generate_external_resource_link(
    cdn_host_url: str,
    resource_tag: str,
    resource_category: str
) -> str:
    """
    Build a fully-qualified URL for a CDN-hosted resource.

    Parameters
    ----------
    cdn_host_url : str
        Base URL of the CDN (e.g. "https://cdn.example.com/").
    resource_tag : str
        Unique identifier for the requested resource.
    resource_category : str
        Category of the resource (e.g. "image", "script").

    Returns
    -------
    str
        Fully-qualified, safe URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If `cdn_host_url` does not resolve to an allowed CDN domain.
    """
    # Parse the base URL and validate scheme
    parsed_base = urllib.parse.urlparse(cdn_host_url)
    if parsed_base.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed_base.scheme}")

    # Ensure the domain is allowed
    base_domain = parsed_base.netloc.lower()
    if not any(base_domain == domain or base_domain.endswith("." + domain)
               for domain in ALLOWED_CDN_DOMAINS):
        raise ValueError(f"Domain '{base_domain}' is not in the allowed CDN list")

    # Build a safe path by joining category and tag
    # urllib.parse.urljoin will correctly handle leading/trailing slashes.
    path = urllib.parse.urljoin("/", f"{resource_category.strip('/')}/{resource_tag.strip('/')}")
    full_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        base_domain,
        path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return full_url


# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Example usage
    try:
        url = generate_external_resource_link(
            cdn_host_url="https://cdn.example.com/",
            resource_tag="logo.png",
            resource_category="image"
        )
        print(url)
    except ValueError as exc:
        print(f"Invalid CDN URL: {exc}")