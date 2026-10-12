import urllib.parse
from typing import Iterable

# Allowed CDN domains (example list; replace with real ones as needed)
ALLOWED_CDN_DOMAINS: Iterable[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.content.org",
}

def create_external_resource_link(cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Assemble a secure URL for an external resource.

    Parameters
    ----------
    cdn_url : str
        Base CDN URL (must be an absolute URL).
    res_id : str
        Unique identifier for the resource.
    res_type : str
        Type of resource (e.g., 'image', 'script').

    Returns
    -------
    str
        A fully-qualified, validated URL pointing to the resource on the CDN.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain not in ALLOWED_CDN_DOMAINS.
    """
    # Parse the base CDN URL to ensure it is absolute and extract its domain
    parsed_base = urllib.parse.urlparse(cdn_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("cdn_url must be an absolute URL with scheme and netloc")

    # Normalize the domain for comparison
    base_domain = parsed_base.netloc.lower()
    if base_domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Unauthorized CDN domain: {base_domain}")

    # Safely encode the resource ID to avoid injection issues
    safe_res_id = urllib.parse.quote(res_id, safe="")

    # Build the relative path; strip any leading/trailing slashes to avoid double slashes
    rel_path = f"{res_type.strip('/')}/{safe_res_id}"

    # Construct the final URL
    full_url = urllib.parse.urljoin(parsed_base.geturl() + "/", rel_path)

    # Final validation: ensure the domain hasn't changed due to join or relative parts
    parsed_final = urllib.parse.urlparse(full_url)
    final_domain = parsed_final.netloc.lower()
    if final_domain != base_domain:
        raise ValueError(f"URL redirects to unauthorized domain: {final_domain}")

    return full_url