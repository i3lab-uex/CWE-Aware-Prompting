import urllib.parse
from typing import Set

# Predefined set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net"
}

def build_external_resource_link(cdn_url: str, resource_key: str, res_category: str) -> str:
    """
    Construct a fully qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the Content Delivery Network (e.g., "https://cdn.example.com").
    resource_key : str
        Identifier of the requested resource (e.g., "logo.png", "app.js").
    res_category : str
        Category/type of the resource (e.g., "image", "script").

    Returns
    -------
    str
        The fully constructed URL pointing to the requested external resource.

    Raises
    ------
    ValueError
        If the resolved CDN domain is not in ``ALLOWED_CDN_DOMAINS``.
    """
    # Parse the base CDN URL to extract components
    parsed_cdn = urllib.parse.urlparse(cdn_url)
    
    # Validate that the domain is allowed
    if parsed_cdn.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"CDN domain '{parsed_cdn.netloc}' is not in the list of allowed domains."
        )

    # Ensure path components are clean (no leading/trailing slashes)
    category = res_category.strip("/")
    key = resource_key.strip("/")

    # Build the path by joining category and resource key
    new_path = urllib.parse.urljoin(f"{parsed_cdn.path.rstrip('/')}/", f"{category}/{key}")

    # Reconstruct the full URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_cdn.scheme,
            parsed_cdn.netloc,
            new_path,
            "",  # params
            "",  # query
            ""   # fragment
        )
    )

    return final_url

# Example usage:
if __name__ == "__main__":
    try:
        url = build_external_resource_link(
            cdn_url="https://cdn.example.com/assets",
            resource_key="logo.png",
            res_category="image"
        )
        print(url)  # https://cdn.example.com/assets/image/logo.png
    except ValueError as e:
        print(f"Invalid CDN: {e}")