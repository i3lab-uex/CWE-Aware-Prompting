import re
from urllib.parse import urlparse, urljoin

# Predefined set of allowed CDN domains (example)
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.safe-cdn.net",
    "static.content.org",
}

# Allowed characters for resource kind (alphanumeric, hyphen, underscore)
_KINDS_REGEX = re.compile(r"^[a-zA-Z0-9_-]+$")


def build_cdn_resource_url(cdn_url: str, resource_identifier: str, resource_kind: str) -> str:
    """
    Construct a full CDN URL for a given resource.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN (e.g., "https://cdn.example.com/").
    resource_identifier : str
        Unique identifier for the requested resource.
    resource_kind : str
        Type of the resource (e.g., "image", "script").

    Returns
    -------
    str
        Fully-qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the base CDN URL does not belong to an allowed domain,
        or if `resource_kind` contains disallowed characters.
    """
    # Validate the resource kind to avoid path traversal or other injection
    if not _KINDS_REGEX.match(resource_kind):
        raise ValueError(f"Invalid resource kind: {resource_kind!r}")

    # Parse the CDN base URL
    parsed_cdn = urlparse(cdn_url)
    if not parsed_cdn.scheme or not parsed_cdn.netloc:
        raise ValueError(f"Malformed CDN URL: {cdn_url!r}")

    # Ensure the CDN domain is allowed
    if parsed_cdn.netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain {parsed_cdn.netloc!r} is not an allowed CDN")

    # Build the relative path: <kind>/<identifier>
    # We ensure no leading slash in components to avoid accidental absolute paths
    relative_path = f"{resource_kind.lstrip('/')}/{resource_identifier.lstrip('/')}"

    # Construct the final URL
    full_url = urljoin(parsed_cdn.geturl(), relative_path)

    # Final sanity check: the resulting URL must still be under an allowed domain
    final_parsed = urlparse(full_url)
    if final_parsed.netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError("Constructed URL points to an unapproved domain")

    return full_url