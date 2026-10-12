import urllib.parse
from typing import Set

# Predefined set of recognized CDN domains that are safe to use.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.cdnprovider.net",
    "static.myapp.org",
}

def create_cdn_resource_link(
    cdn_url_base: str,
    resource_identifier: str,
    type_of_resource: str
) -> str:
    """
    Construct a secure CDN URL for a given resource.

    Parameters
    ----------
    cdn_url_base : str
        The base URL of the CDN (e.g. "https://cdn.example.com/").
    resource_identifier : str
        Identifier of the requested resource (e.g. "images/logo.png").
    type_of_resource : str
        Type of the resource (e.g. "image", "script"). This is not used in
        URL construction but may be validated for future extensions.

    Returns
    -------
    str
        Fully constructed, absolute URL pointing to the resource.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain not present in
        `ALLOWED_CDN_DOMAINS`.
    """
    # Sanity check for type_of_resource (optional)
    if not isinstance(type_of_resource, str):
        raise TypeError("type_of_resource must be a string")

    # Build the URL using urllib.parse.urljoin to correctly handle slashes.
    full_url = urllib.parse.urljoin(cdn_url_base.rstrip('/') + '/', resource_identifier.lstrip('/'))

    # Parse the URL to inspect its components.
    parsed = urllib.parse.urlparse(full_url)

    # Ensure we have a network location (netloc) and it's allowed.
    netloc = parsed.netloc.lower()
    if not netloc or netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {netloc}")

    # Return the fully resolved URL.
    return full_url