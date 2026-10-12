import urllib.parse
from typing import Set

# Allowed CDN domains – extend as needed.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.cdnprovider.org",
}

def create_external_resource_link(cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Assemble a validated URL for an external resource.

    Parameters
    ----------
    cdn_url : str
        Base CDN URL (e.g., "https://cdn.example.com/").
    res_id : str
        Unique identifier for the resource.
    res_type : str
        Resource type such as 'image', 'script', etc.

    Returns
    -------
    str
        Fully qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain not in ALLOWED_CDN_DOMAINS.
    """
    # Parse the base CDN URL and ensure it has a scheme.
    parsed_cdn = urllib.parse.urlparse(cdn_url)
    if not parsed_cdn.scheme:
        raise ValueError(f"cdn_url must include a scheme (http/https): {cdn_url}")

    # Normalise the path to avoid double slashes.
    base_path = parsed_cdn.path.rstrip("/") + "/"

    # Construct the relative path for the resource.
    # Example: "image/abc123.jpg"
    resource_path = urllib.parse.quote(f"{res_type}/{res_id}")

    # Build the full URL.
    full_url = urllib.parse.urlunparse((
        parsed_cdn.scheme,
        parsed_cdn.netloc,
        urllib.parse.urljoin(base_path, resource_path),
        "",  # params
        "",  # query
        ""   # fragment
    ))

    # Validate the domain.
    if parsed_cdn.netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Unauthorized CDN domain: {parsed_cdn.netloc}")

    return full_url