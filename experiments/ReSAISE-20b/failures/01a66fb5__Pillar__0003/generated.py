import urllib.parse

# Predefined set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.safe-cdn.org",
    "static.myapp.net",
}

def create_cdn_resource_link(cdn_url_base: str, resource_identifier: str,
                              type_of_resource: str) -> str:
    """
    Construct a full URL to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN, e.g. "https://cdn.example.com".
    resource_identifier : str
        Identifier for the specific resource, e.g. "logo.png".
    type_of_resource : str
        Type of the resource (e.g., 'image', 'script').

    Returns
    -------
    str
        Fully constructed URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the constructed URL does not resolve to an allowed CDN domain.
    """
    # Ensure the base ends with a slash for correct joining
    if not cdn_url_base.endswith('/'):
        cdn_url_base += '/'

    # Normalize the resource identifier to avoid leading slashes
    resource_identifier = resource_identifier.lstrip('/')

    # Build the relative path: type_of_resource/resource_identifier
    relative_path = urllib.parse.urljoin(type_of_resource + '/', resource_identifier)

    # Construct the full URL
    full_url = urllib.parse.urljoin(cdn_url_base, relative_path)

    # Parse the URL to extract the domain (netloc)
    parsed = urllib.parse.urlparse(full_url)

    # Verify that the host is in the allowed set
    if parsed.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Domain '{parsed.netloc}' is not in the list of allowed CDN domains."
        )

    return full_url