import urllib.parse

# Example set of allowed CDN domains. In a real application this should be defined elsewhere.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.content.org"
}

def create_cdn_resource_link(cdn_url_base: str,
                              resource_identifier: str,
                              type_of_resource: str) -> str:
    """
    Construct a secure CDN URL for a given resource.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN (e.g. "https://cdn.example.com/").
    resource_identifier : str
        Identifier of the resource (e.g. a file name or hash).
    type_of_resource : str
        Type of the resource (e.g. "image", "script").

    Returns
    -------
    str
        Fully constructed CDN URL.

    Raises
    ------
    ValueError
        If the resulting URL points to a domain not in ``ALLOWED_CDN_DOMAINS``.
    """
    # Ensure base URL ends with a slash to allow proper joining
    if not cdn_url_base.endswith('/'):
        cdn_url_base += '/'

    # Normalize type_of_resource to avoid leading/trailing slashes
    resource_type = type_of_resource.strip('/')

    # Normalize resource_identifier: strip leading slashes, encode special chars
    safe_resource_id = urllib.parse.quote(resource_identifier.strip('/'))

    # Build the relative path: type_of_resource/resource_identifier
    relative_path = f"{resource_type}/{safe_resource_id}"

    # Join base URL and relative path
    full_url = urllib.parse.urljoin(cdn_url_base, relative_path)

    # Parse the resulting URL to extract the domain (netloc)
    parsed = urllib.parse.urlparse(full_url)

    # Extract hostname without port
    hostname = parsed.hostname

    if not hostname or hostname.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {hostname!r}")

    return full_url