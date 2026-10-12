import urllib.parse

# Define a set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.safe-cdn.org",
    "static.content.net",
}

def build_external_resource_link(cdn_url: str, resource_key: str, res_category: str) -> str:
    """
    Construct a URL to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN, e.g. "https://cdn.example.com".
    resource_key : str
        Identifier of the requested resource (e.g. "logo.png").
    res_category : str
        Category of the resource, used to form a sub‑path (e.g. "image").

    Returns
    -------
    str
        Fully qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the parsed CDN domain is not in ``ALLOWED_CDN_DOMAINS``.
    """
    # Parse the base CDN URL
    parsed_cdn = urllib.parse.urlparse(cdn_url)
    if not parsed_cdn.scheme or not parsed_cdn.netloc:
        raise ValueError(f"Invalid CDN URL: {cdn_url!r}")

    # Normalize the domain (strip port if present)
    netloc = parsed_cdn.netloc.split(":")[0]
    if netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain {netloc!r} is not an allowed CDN domain")

    # Build the path to the resource
    # Ensure that res_category and resource_key are safely joined
    safe_res_cat = urllib.parse.quote(res_category.strip("/"))
    safe_resource_key = urllib.parse.quote(resource_key.strip("/"))

    # Join the path components
    resource_path = "/".join([safe_res_cat, safe_resource_key])

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

# Example usage:
if __name__ == "__main__":
    try:
        url = build_external_resource_link(
            cdn_url="https://cdn.example.com/assets",
            resource_key="logo.png",
            res_category="images"
        )
        print(url)  # Expected: https://cdn.example.com/assets/images/logo.png
    except ValueError as e:
        print(f"URL construction failed: {e}")