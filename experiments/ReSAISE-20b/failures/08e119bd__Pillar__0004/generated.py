import urllib.parse

# Predefined set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.cdnprovider.net",
    "static.myapp.org",
}

def generate_external_resource_link(cdn_host_url: str, resource_tag: str, resource_category: str) -> str:
    """
    Construct a full URL to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_host_url : str
        Base URL of the CDN (e.g. "https://cdn.example.com/").
    resource_tag : str
        Unique identifier for the requested resource (e.g. "logo.png").
    resource_category : str
        Category of the resource, used to build the path (e.g. "image", "script").

    Returns
    -------
    str
        A fully resolved URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resolved URL does not belong to an allowed CDN domain.
    """
    # Sanitize inputs: strip whitespace and ensure they are non-empty
    if not (cdn_host_url and resource_tag and resource_category):
        raise ValueError("All arguments must be non-empty strings")

    # Ensure the CDN host URL ends with a slash for correct joining
    base_url = cdn_host_url.rstrip('/') + '/'

    # Construct the relative path in a safe manner
    # Use urllib.parse.quote to escape any problematic characters
    rel_path = urllib.parse.urljoin(
        f"{resource_category.rstrip('/')}/",
        urllib.parse.quote(resource_tag, safe='')
    )

    # Resolve the full URL
    full_url = urllib.parse.urljoin(base_url, rel_path)

    # Parse the resulting URL to extract the domain
    parsed = urllib.parse.urlparse(full_url)

    # Validate that the host is in the allowed set
    if parsed.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {parsed.netloc}")

    # Return the normalized URL (scheme + netloc + path)
    return urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        '',  # params
        '',  # query
        ''   # fragment
    ))