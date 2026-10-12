import urllib.parse

# Example set of allowed CDN domains. In real code this would be defined elsewhere.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.anothercdn.net",
}

def create_cdn_resource_link(cdn_url_base: str, resource_identifier: str, type_of_resource: str) -> str:
    """
    Construct a secure URL pointing to an external resource on a CDN.

    Parameters
    ----------
    cdn_url_base : str
        The base URL of the CDN (e.g., "https://cdn.example.com/").
    resource_identifier : str
        The identifier of the resource (e.g., "12345" or a path fragment).
    type_of_resource : str
        The resource type, used to build the path (e.g., "image", "script").

    Returns
    -------
    str
        A fully-qualified URL pointing to the resource.

    Raises
    ------
    ValueError
        If the constructed URL does not resolve to an allowed CDN domain.
    """
    # Ensure base ends with a slash for proper urljoin behavior
    if not cdn_url_base.endswith("/"):
        base = f"{cdn_url_base}/"
    else:
        base = cdn_url_base

    # Build the relative path: type_of_resource/resource_identifier
    rel_path = urllib.parse.urljoin(f"{type_of_resource}/", resource_identifier)

    # Construct the full URL
    full_url = urllib.parse.urljoin(base, rel_path)

    # Parse the domain from the URL
    parsed = urllib.parse.urlparse(full_url)
    netloc = parsed.netloc.lower()

    # Strip port if present
    domain = netloc.split(":")[0]

    # Validate against allowed domains
    if domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {domain}")

    return full_url