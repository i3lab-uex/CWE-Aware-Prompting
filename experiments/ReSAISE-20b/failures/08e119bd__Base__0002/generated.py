import urllib.parse

# Set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.contenthost.org",
}

def generate_external_resource_link(
    cdn_host_url: str,
    resource_tag: str,
    resource_category: str
) -> str:
    """
    Construct a full URL to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_host_url : str
        Base URL of the CDN (e.g. "https://cdn.example.com").
    resource_tag : str
        Unique identifier for the requested resource.
    resource_category : str
        Category/type of the resource (e.g. "image", "script").

    Returns
    -------
    str
        Fully-qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the CDN host domain is not in ``ALLOWED_CDN_DOMAINS`` or if
        any part of the URL is malformed.
    """
    # Parse the CDN host URL to extract scheme and netloc
    parsed_cdn = urllib.parse.urlparse(cdn_host_url)

    # Ensure the URL has a scheme (http or https) and a netloc
    if not parsed_cdn.scheme or not parsed_cdn.netloc:
        raise ValueError(f"Invalid CDN host URL: {cdn_host_url}")

    # Normalize the domain (remove any port, subdomains are preserved)
    netloc = parsed_cdn.hostname
    if not netloc:
        raise ValueError(f"Unable to determine hostname from CDN URL: {cdn_host_url}")

    # Verify that the domain is in the whitelist
    if netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {netloc}")

    # Build the path ensuring no double slashes
    path_parts = [
        resource_category.strip("/"),
        resource_tag.strip("/")
    ]
    resource_path = "/".join(path_parts)

    # Construct the final URL
    final_url = urllib.parse.urlunparse((
        parsed_cdn.scheme,
        parsed_cdn.netloc,
        urllib.parse.urljoin(parsed_cdn.path + "/", resource_path),
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return final_url