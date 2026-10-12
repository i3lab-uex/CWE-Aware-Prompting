import urllib.parse

# Set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.safe-cdn.org",
    # Add other trusted domains here.
}


def construct_external_resource_url(cdn_base_url: str, resource_id: str, resource_type: str) -> str:
    """
    Construct a fully-qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base_url : str
        The base URL of the CDN.  Must include scheme (http:// or https://).
    resource_id : str
        The unique identifier of the resource to fetch.
    resource_type : str
        The type of resource (e.g., 'image', 'script').  Used as a path segment.

    Returns
    -------
    str
        The absolute URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL does not point to an allowed CDN domain.
    """
    # Sanitize inputs by ensuring they are strings and stripping whitespace
    if not isinstance(cdn_base_url, str):
        raise TypeError("cdn_base_url must be a string")
    if not isinstance(resource_id, str):
        raise TypeError("resource_id must be a string")
    if not isinstance(resource_type, str):
        raise TypeError("resource_type must be a string")

    cdn_base_url = cdn_base_url.strip()
    resource_id = urllib.parse.quote(resource_id.strip(), safe="")
    resource_type = urllib.parse.quote(resource_type.strip(), safe="")

    # Build the relative path: /{resource_type}/{resource_id}
    relative_path = urllib.parse.urljoin("/", f"{resource_type}/")
    full_url = urllib.parse.urljoin(cdn_base_url.rstrip("/") + "/", f"{resource_type}/{resource_id}")

    # Parse the URL to extract the domain
    parsed = urllib.parse.urlparse(full_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Constructed URL is malformed")

    # Ensure the domain is in the allowed list (case-insensitive)
    domain = parsed.hostname.lower()
    if domain not in {d.lower() for d in ALLOWED_CDN_DOMAINS}:
        raise ValueError(f"Disallowed CDN domain: {domain}")

    return full_url