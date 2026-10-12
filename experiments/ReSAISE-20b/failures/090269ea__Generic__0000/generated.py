import urllib.parse
from typing import Iterable

# Set of CDN domains that are allowed to be used.
ALLOWED_CDN_DOMAINS: Iterable[str] = {
    "cdn.example.com",
    "assets.cdn.net",
    "static.content.org",
}

def create_external_resource_link(cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Build a fully qualified URL to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN. It can be a full URL (including scheme) or just a hostname.
    res_id : str
        Unique identifier of the resource. May contain characters that need to be URL‑encoded.
    res_type : str
        Type of resource being requested (e.g., 'image', 'script'). Used to construct the path.

    Returns
    -------
    str
        A fully resolved, scheme‑prefixed URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain not in :data:`ALLOWED_CDN_DOMAINS`.
    """
    # Ensure the CDN URL has a scheme; default to https if missing
    parsed_cdn = urllib.parse.urlparse(cdn_url)
    scheme = parsed_cdn.scheme or "https"
    netloc = parsed_cdn.netloc or parsed_cdn.path  # handles bare hostnames
    if not netloc:
        raise ValueError("Invalid CDN URL provided")

    # Validate the domain against the allowed list
    if netloc.lower() not in (d.lower() for d in ALLOWED_CDN_DOMAINS):
        raise ValueError(f"Domain '{netloc}' is not an authorized CDN domain")

    # Build the resource path safely
    safe_res_id = urllib.parse.quote(res_id, safe="")
    path_parts = [parsed_cdn.path.rstrip("/"), res_type.strip("/"), safe_res_id]
    resource_path = "/".join(filter(None, path_parts))

    # Reconstruct the full URL
    final_url = urllib.parse.urlunparse(
        (scheme, netloc, resource_path, "", "", "")
    )
    return final_url