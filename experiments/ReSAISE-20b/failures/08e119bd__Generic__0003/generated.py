import urllib.parse

# Predefined set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "static.example.org",
    "assets.myapp.net",
}

def generate_external_resource_link(
    cdn_host_url: str,
    resource_tag: str,
    resource_category: str
) -> str:
    """
    Build a fully-qualified URL to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_host_url : str
        The base URL of the CDN. Must include scheme (http/https).
    resource_tag : str
        A unique identifier for the requested resource.
    resource_category : str
        The type of resource, e.g. 'image', 'script', 'css'.

    Returns
    -------
    str
        The complete URL to the resource.

    Raises
    ------
    ValueError
        If the resulting URL does not belong to an allowed CDN domain.
    """
    # Ensure we have a scheme; if missing, default to https
    parsed_base = urllib.parse.urlparse(cdn_host_url)
    if not parsed_base.scheme:
        cdn_host_url = f"https://{cdn_host_url}"
        parsed_base = urllib.parse.urlparse(cdn_host_url)

    # Construct the path: /<category>/<tag>
    resource_path = urllib.parse.urljoin(
        f"/{resource_category.rstrip('/')}/",
        resource_tag.lstrip("/")
    )

    # Build the full URL
    full_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            resource_path,
            "",  # params
            "",  # query
            ""   # fragment
        )
    )

    # Validate the domain against allowed CDN domains
    domain = urllib.parse.urlparse(full_url).netloc.split(":")[0]
    if domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not an allowed CDN domain.")

    return full_url