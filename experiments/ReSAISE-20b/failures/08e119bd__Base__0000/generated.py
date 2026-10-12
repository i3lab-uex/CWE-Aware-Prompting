import urllib.parse
from typing import Set

# Predefined set of allowed CDN domains (example)
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.safe-cdn.org",
    "images.public.net",
}

def generate_external_resource_link(
    cdn_host_url: str,
    resource_tag: str,
    resource_category: str
) -> str:
    """
    Construct a full URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_host_url : str
        Base URL of the CDN (e.g. "https://cdn.example.com").
    resource_tag : str
        Unique identifier for the requested resource.
    resource_category : str
        Category of the resource (e.g. "image", "script").

    Returns
    -------
    str
        Fully-qualified URL to the resource.

    Raises
    ------
    ValueError
        If the constructed URL does not belong to an allowed CDN domain.
    """
    # Parse the base CDN URL
    parsed_cdn = urllib.parse.urlparse(cdn_host_url)

    # Ensure scheme is http or https
    if parsed_cdn.scheme not in {"http", "https"}:
        raise ValueError("CDN URL must use http or https scheme")

    # Validate the CDN domain
    if parsed_cdn.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"CDN host '{parsed_cdn.hostname}' is not allowed")

    # Safely encode path components
    encoded_category = urllib.parse.quote(resource_category.strip("/"))
    encoded_tag = urllib.parse.quote(resource_tag.strip("/"))

    # Build the new path
    # Example: /images/abc123.png
    path = urllib.parse.urljoin(parsed_cdn.path + "/", f"{encoded_category}/{encoded_tag}")

    # Reconstruct the full URL
    final_url = urllib.parse.urlunparse((
        parsed_cdn.scheme,
        parsed_cdn.netloc,
        path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return final_url