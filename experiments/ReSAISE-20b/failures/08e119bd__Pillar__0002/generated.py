import urllib.parse
from typing import Set

# Predefined set of domains considered safe for CDNs.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "static.myapp.org",
    "assets.partner.net"
}

def generate_external_resource_link(
    cdn_host_url: str,
    resource_tag: str,
    resource_category: str
) -> str:
    """
    Build a fully-qualified URL to fetch an external resource from a CDN.

    Parameters
    ----------
    cdn_host_url : str
        Base URL of the CDN (e.g. "https://cdn.example.com").
    resource_tag : str
        Unique identifier of the requested resource.
    resource_category : str
        Category of the resource, e.g. "image" or "script".

    Returns
    -------
    str
        The absolute URL pointing to the resource on the CDN.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain not in ALLOWED_CDN_DOMAINS.
    """
    # Sanitize inputs
    if not isinstance(cdn_host_url, str):
        raise TypeError("cdn_host_url must be a string")
    if not isinstance(resource_tag, str):
        raise TypeError("resource_tag must be a string")
    if not isinstance(resource_category, str):
        raise TypeError("resource_category must be a string")

    # Ensure the host URL ends with a slash so urljoin works correctly
    if not cdn_host_url.endswith("/"):
        cdn_host_url += "/"

    # Percent‑encode the path components to avoid injection
    safe_tag = urllib.parse.quote_plus(resource_tag)
    safe_category = urllib.parse.quote_plus(resource_category)

    # Construct the relative path
    relative_path = f"{safe_category}/{safe_tag}"

    # Build the absolute URL
    full_url = urllib.parse.urljoin(cdn_host_url, relative_path)

    # Validate the domain
    parsed = urllib.parse.urlparse(full_url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL scheme must be http or https")

    domain = parsed.netloc.split(":")[0]  # strip port if present
    if domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {domain}")

    return full_url