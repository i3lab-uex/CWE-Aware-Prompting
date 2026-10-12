import urllib.parse
from typing import Set

# A set of CDN domains that are allowed to be used.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.provider.net",
}

# Optional whitelist of allowed resource types
ALLOWED_RESOURCE_TYPES: Set[str] = {"image", "script", "style", "font"}


def construct_external_resource_url(
    cdn_base_url: str, resource_id: str, resource_type: str
) -> str:
    """
    Construct a fully qualified URL to an external resource on a CDN.

    Parameters
    ----------
    cdn_base_url : str
        The base URL of the CDN (e.g. "https://cdn.example.com/").
    resource_id : str
        The identifier of the resource to fetch (e.g. "logo.png").
    resource_type : str
        The type of the resource, used for validation (e.g. "image").

    Returns
    -------
    str
        The complete URL to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL points to a domain not in :data:`ALLOWED_CDN_DOMAINS`
        or if the resource type is not allowed.
    """
    # Validate the resource type
    if resource_type.lower() not in ALLOWED_RESOURCE_TYPES:
        raise ValueError(f"Unsupported resource type: {resource_type!r}")

    # Ensure the base URL has a scheme
    parsed_base = urllib.parse.urlparse(cdn_base_url)
    if not parsed_base.scheme:
        raise ValueError(f"Base CDN URL must include a scheme (http/https): {cdn_base_url!r}")

    # Normalize the base URL to ensure it ends with a slash
    if not cdn_base_url.endswith("/"):
        cdn_base_url += "/"

    # Build the full URL
    full_url = urllib.parse.urljoin(cdn_base_url, resource_id)

    # Parse the resulting URL to validate its domain
    parsed_full = urllib.parse.urlparse(full_url)
    if not parsed_full.scheme or not parsed_full.netloc:
        raise ValueError(f"Malformed URL generated: {full_url!r}")

    # Check if the domain is in the allowed set
    hostname = parsed_full.hostname.lower()
    if hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Disallowed CDN domain: {hostname!r}. Allowed domains are: "
            f"{', '.join(sorted(ALLOWED_CDN_DOMAINS))}"
        )

    # Ensure the path does not contain any relative traversal segments
    if ".." in parsed_full.path.split("/"):
        raise ValueError(f"URL path contains disallowed traversal: {parsed_full.path!r}")

    return full_url