import urllib.parse

# Set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "static.mysite.org",
    "assets.anotherdomain.net",
}

def build_external_resource_link(cdn_url: str, resource_key: str, res_category: str) -> str:
    """
    Construct a fully-qualified URL pointing to an external resource on a CDN.

    Parameters
    ----------
    cdn_url : str
        The base URL of the CDN (e.g., "https://cdn.example.com").
    resource_key : str
        Identifier of the requested resource (e.g., "images/logo.png").
    res_category : str
        Category of the resource, such as 'image' or 'script'.

    Returns
    -------
    str
        The complete URL that can be used to fetch the resource.

    Raises
    ------
    ValueError
        If the resulting URL does not target a domain in ALLOWED_CDN_DOMAINS,
        or if the resource_key is malformed (contains path traversal).
    """
    # Validate inputs
    if not isinstance(cdn_url, str) or not isinstance(resource_key, str) or not isinstance(res_category, str):
        raise TypeError("All arguments must be strings.")

    # Ensure resource_key does not contain path traversal or protocol indicators
    if ".." in resource_key or "://" in resource_key:
        raise ValueError("Invalid resource key: contains disallowed patterns.")

    # Parse the CDN base URL
    parsed_cdn = urllib.parse.urlparse(cdn_url)

    # Verify that the CDN domain is allowed
    if parsed_cdn.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {parsed_cdn.hostname}")

    # Build the path: /<res_category>/<resource_key>
    # Ensure leading slash and no duplicate slashes
    path = urllib.parse.urljoin(f"/{res_category}/", resource_key.lstrip("/"))

    # Reconstruct the full URL
    final_url = urllib.parse.urlunparse((
        parsed_cdn.scheme,
        parsed_cdn.netloc,
        path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return final_url

# Example usage:
if __name__ == "__main__":
    url = build_external_resource_link(
        "https://cdn.example.com",
        "images/logo.png",
        "image"
    )
    print(url)   # Outputs: https://cdn.example.com/image/images/logo.png