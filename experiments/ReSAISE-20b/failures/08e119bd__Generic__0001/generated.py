import urllib.parse

# Example allowed CDN domains – adjust as needed for your environment.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.contentprovider.org",
}

def generate_external_resource_link(
    cdn_host_url: str,
    resource_tag: str,
    resource_category: str
) -> str:
    """
    Build a full CDN URL for the requested resource.

    Parameters
    ----------
    cdn_host_url : str
        Base URL of the CDN (e.g. "https://cdn.example.com").
    resource_tag : str
        Unique identifier for the resource (e.g. "logo.png").
    resource_category : str
        Category of the resource, typically a directory name
        (e.g. "image" or "script").

    Returns
    -------
    str
        The fully-qualified URL pointing to the resource.

    Raises
    ------
    ValueError
        If the constructed URL does not belong to an allowed CDN domain.
    """
    # Ensure the base URL has a scheme; default to https if missing
    parsed_base = urllib.parse.urlparse(cdn_host_url)
    if not parsed_base.scheme:
        cdn_host_url = f"https://{cdn_host_url}"
        parsed_base = urllib.parse.urlparse(cdn_host_url)

    # Sanitize and join the path components
    # Use urllib.parse.urljoin to correctly handle slashes
    relative_path = f"/{resource_category.strip('/')}/{resource_tag.lstrip('/')}"
    full_url = urllib.parse.urljoin(cdn_host_url.rstrip("/") + "/", relative_path.lstrip("/"))

    # Validate that the netloc (domain) is allowed
    domain = urllib.parse.urlparse(full_url).netloc.lower()
    if domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Disallowed CDN domain '{domain}'. "
            f"Allowed domains are: {', '.join(sorted(ALLOWED_CDN_DOMAINS))}"
        )

    return full_url