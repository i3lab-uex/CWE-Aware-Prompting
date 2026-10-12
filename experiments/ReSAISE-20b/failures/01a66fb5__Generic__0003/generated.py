import urllib.parse
from typing import Set

# Predefined set of allowed CDN domains (example values)
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.mywebsite.org",
    "static.thirdparty.net"
}


def create_cdn_resource_link(
    cdn_url_base: str,
    resource_identifier: str,
    type_of_resource: str
) -> str:
    """
    Construct a fully-qualified CDN URL for a given resource.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN (e.g. 'https://cdn.example.com/base/path').
    resource_identifier : str
        Identifier of the requested resource (e.g. 'logo.png', 'app.js').
    type_of_resource : str
        Type of the resource, used to build a logical path (e.g. 'image', 'script').

    Returns
    -------
    str
        The fully constructed URL pointing to the external resource.

    Raises
    ------
    ValueError
        If the domain of `cdn_url_base` is not in :data:`ALLOWED_CDN_DOMAINS`.
    """
    # Parse the base URL
    parsed_base = urllib.parse.urlparse(cdn_url_base)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_url_base!r}")

    # Ensure the domain is allowed
    domain = parsed_base.netloc.lower()
    if domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not an allowed CDN domain")

    # Build the path
    # Normalize existing path: strip trailing slashes, then add type and identifier
    base_path = parsed_base.path.rstrip("/")
    # Use urllib.parse.quote to safely encode path components
    type_path = urllib.parse.quote(type_of_resource.strip("/"))
    resource_path = urllib.parse.quote(resource_identifier.strip("/"))

    full_path = f"{base_path}/{type_path}/{resource_path}"

    # Reconstruct the URL, preserving any query or fragment from the base
    final_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        parsed_base.params,
        parsed_base.query,
        parsed_base.fragment
    ))

    return final_url


# Example usage (uncomment to test):
# print(create_cdn_resource_link(
#     "https://cdn.example.com/assets",
#     "logo.png",
#     "image"
# ))