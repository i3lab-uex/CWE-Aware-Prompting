import urllib.parse
from pathlib import Path

# Set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "static.myapp.net",
    "assets.otherdomain.org"
}

def build_external_resource_link(cdn_url: str, resource_key: str, res_category: str) -> str:
    """
    Construct a full URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the Content Delivery Network (e.g., "https://cdn.example.com").
    resource_key : str
        Identifier for the specific resource (may contain sub‑paths).
    res_category : str
        Category of the resource, e.g. "image", "script".

    Returns
    -------
    str
        Fully resolved URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in ALLOWED_CDN_DOMAINS
        or if the constructed path attempts directory traversal.
    """
    # Ensure the CDN base URL has a scheme
    if not urllib.parse.urlparse(cdn_url).scheme:
        cdn_url = "https://" + cdn_url

    # Encode the resource key to avoid injection of raw slashes or unsafe characters
    encoded_key = urllib.parse.quote(resource_key, safe="")

    # Build a relative path: /{category}/{encoded_key}
    rel_path = urllib.parse.urljoin(f"/{res_category}/", encoded_key)

    # Join with the CDN base URL
    full_url = urllib.parse.urljoin(cdn_url.rstrip('/') + "/", rel_path.lstrip('/'))

    # Parse the resulting URL to validate its components
    parsed = urllib.parse.urlparse(full_url)

    # 1. Domain check – ensure the hostname is allowed
    if parsed.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{parsed.hostname}' is not in the list of allowed CDN domains.")

    # 2. Path traversal check – disallow any '..' components
    path = Path(parsed.path)
    if ".." in path.parts:
        raise ValueError("Path traversal detected in the constructed URL.")

    return full_url