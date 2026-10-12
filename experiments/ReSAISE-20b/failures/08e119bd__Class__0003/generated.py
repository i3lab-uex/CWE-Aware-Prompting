import urllib.parse

# Example set of allowed CDN domains. Replace with the real list.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net"
}

def generate_external_resource_link(cdn_host_url: str,
                                     resource_tag: str,
                                     resource_category: str) -> str:
    """
    Build a fully qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_host_url : str
        The base URL of the CDN (e.g., "https://cdn.example.com").
    resource_tag : str
        A unique identifier for the requested resource (e.g., "logo.png").
    resource_category : str
        The type of resource, used to build the path (e.g., "image" or "script").

    Returns
    -------
    str
        The fully qualified URL pointing to the resource.

    Raises
    ------
    ValueError
        If the constructed URL does not resolve to an allowed CDN domain.
    """
    # Normalise inputs
    cdn_host_url = cdn_host_url.rstrip("/")
    resource_tag = resource_tag.lstrip("/")
    resource_category = resource_category.strip("/")

    # Build the relative path: <category>/<tag>
    rel_path = urllib.parse.urljoin(f"{resource_category}/", resource_tag)

    # Construct the full URL
    full_url = urllib.parse.urljoin(cdn_host_url + "/", rel_path)

    # Parse the URL to inspect its components
    parsed = urllib.parse.urlparse(full_url)

    # Ensure that the netloc (domain) is in the allowed set
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # The domain may contain a port; strip it for comparison
    host = parsed.hostname or ""
    if host.lower() not in {d.lower() for d in ALLOWED_CDN_DOMAINS}:
        raise ValueError(f"Disallowed CDN domain: {host}")

    # Return the sanitized, fully qualified URL
    return full_url