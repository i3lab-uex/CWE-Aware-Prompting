import urllib.parse

# Predefined set of domains that are considered safe CDNs.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.content.org",
}

def create_resource_url(base_cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Construct a fully-qualified CDN URL for a given resource.

    Parameters
    ----------
    base_cdn_url : str
        The base URL of the CDN (e.g., "https://cdn.example.com").
    res_id : str
        The unique identifier for the resource (e.g., "12345").
    res_type : str
        The type of resource, used as a path segment (e.g., "image", "script").

    Returns
    -------
    str
        The fully-qualified URL to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to an allowed CDN domain.
    """
    # Parse the base URL and ensure it has a scheme
    parsed_base = urllib.parse.urlparse(base_cdn_url)
    if not parsed_base.scheme:
        raise ValueError("Base CDN URL must include a scheme (e.g., 'https://').")

    # Normalise the path to avoid accidental double slashes
    base_path = parsed_base.path.rstrip("/")
    res_type_clean = urllib.parse.quote(res_type.strip("/"))
    res_id_clean = urllib.parse.quote(res_id.strip("/"))

    # Build the relative path: <res_type>/<res_id>
    relative_path = f"{res_type_clean}/{res_id_clean}"

    # Construct the full URL
    full_url = urllib.parse.urljoin(parsed_base.geturl() + "/", relative_path)

    # Validate that the host is an allowed CDN domain
    host = urllib.parse.urlparse(full_url).hostname
    if not host or host.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"URL host '{host}' is not an allowed CDN domain.")

    return full_url