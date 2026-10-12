import urllib.parse

# Set of CDN domains that are considered safe and allowed.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.cdn.io",
}

def generate_external_resource_link(
    cdn_host_url: str,
    resource_tag: str,
    resource_category: str
) -> str:
    """
    Build a secure URL pointing to an external CDN resource.

    Parameters
    ----------
    cdn_host_url : str
        Base URL of the CDN, e.g. "https://cdn.example.com".
    resource_tag : str
        Unique identifier of the requested resource.
    resource_category : str
        Type/category of the resource, e.g. "image", "script".

    Returns
    -------
    str
        Fully-qualified URL pointing to the resource.

    Raises
    ------
    ValueError
        If the resulting URL does not belong to an allowed CDN domain.
    """
    # Parse the provided CDN host URL
    parsed_cdn = urllib.parse.urlparse(cdn_host_url)

    # Ensure the CDN host has a scheme and netloc
    if not parsed_cdn.scheme or not parsed_cdn.netloc:
        raise ValueError("cdn_host_url must include a scheme (e.g., https://) and host")

    # Verify that the CDN domain is in the allowed set
    if parsed_cdn.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{parsed_cdn.hostname}' is not an allowed CDN")

    # Normalise the resource path: avoid double slashes
    resource_path = urllib.parse.urljoin(
        f"/{resource_category.rstrip('/')}/",
        resource_tag.lstrip("/")
    )

    # Construct the final URL
    full_url = urllib.parse.urlunparse((
        parsed_cdn.scheme,
        parsed_cdn.netloc,
        resource_path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return full_url

# Example usage:
if __name__ == "__main__":
    url = generate_external_resource_link(
        "https://cdn.example.com",
        "12345/logo.png",
        "image"
    )
    print(url)  # https://cdn.example.com/image/12345/logo.png