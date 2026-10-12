import urllib.parse
from typing import Set

# Predefined set of allowed CDN domains
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net",
}

def create_resource_url(base_cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Construct a fully-qualified URL for a CDN-hosted resource.

    Parameters
    ----------
    base_cdn_url : str
        The base URL of the CDN (e.g., "https://cdn.example.com").
    res_id : str
        The unique identifier of the resource (e.g., "logo.svg").
    res_type : str
        The type/category of the resource (e.g., "image", "script").

    Returns
    -------
    str
        The fully-qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to an allowed CDN domain.
    """
    # Sanitize inputs: strip whitespace and ensure no leading/trailing slashes
    base_cdn_url = base_cdn_url.strip()
    res_id = res_id.strip().lstrip("/")
    res_type = res_type.strip().rstrip("/")

    # Build the path: <res_type>/<res_id>
    resource_path = urllib.parse.urljoin(f"{res_type}/", res_id)

    # Construct the full URL
    full_url = urllib.parse.urljoin(base_cdn_url.rstrip("/") + "/", resource_path)

    # Parse the resulting URL to extract the hostname
    parsed = urllib.parse.urlparse(full_url)
    hostname = parsed.hostname

    if not hostname:
        raise ValueError("Constructed URL does not contain a valid hostname.")

    # Ensure the hostname is in the allowed set
    if hostname.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"URL domain '{hostname}' is not in the list of allowed CDN domains."
        )

    return full_url