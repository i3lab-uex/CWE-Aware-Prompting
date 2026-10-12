import urllib.parse
from typing import Set

# Example set of allowed CDN domains.  In a real application this would
# be defined elsewhere and kept in sync with the deployment configuration.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.content-provider.org",
}

def generate_external_resource_link(
    cdn_host_url: str,
    resource_tag: str,
    resource_category: str
) -> str:
    """
    Build a fully-qualified URL for a CDN-hosted resource.

    Parameters
    ----------
    cdn_host_url : str
        Base URL of the CDN, e.g. "https://cdn.example.com".
    resource_tag : str
        Unique identifier for the requested resource.
    resource_category : str
        Category of the resource (e.g., "image", "script").

    Returns
    -------
    str
        The fully-qualified URL to the requested resource.

    Raises
    ------
    ValueError
        If the resolved host is not part of :data:`ALLOWED_CDN_DOMAINS`.

    Notes
    -----
    The function normalises the input URLs to avoid accidental path traversal or
    double‑slashing.  It also verifies that the final host matches one of the
    allowed CDN domains to mitigate DNS rebinding and other domain‑spoofing
    attacks.
    """
    # Sanity check: all arguments must be non-empty strings.
    if not all(isinstance(arg, str) and arg for arg in (cdn_host_url, resource_tag, resource_category)):
        raise ValueError("All arguments must be non-empty strings")

    # Normalise the CDN host URL
    parsed_cdn = urllib.parse.urlparse(cdn_host_url)
    if not parsed_cdn.scheme or not parsed_cdn.netloc:
        raise ValueError(f"Invalid CDN host URL: {cdn_host_url!r}")

    # Build the relative path for the resource.
    # Use urllib.parse.quote to avoid injection via special characters.
    safe_tag = urllib.parse.quote(resource_tag, safe="")
    safe_category = urllib.parse.quote(resource_category, safe="")

    relative_path = f"/{safe_category}/{safe_tag}"

    # Join the CDN host with the relative path.
    full_url = urllib.parse.urljoin(parsed_cdn.geturl(), relative_path)

    # Validate the host against the allowed CDN domains.
    final_parsed = urllib.parse.urlparse(full_url)
    host = final_parsed.hostname
    if not host or host.lower() not in (d.lower() for d in ALLOWED_CDN_DOMAINS):
        raise ValueError(f"Disallowed CDN host: {host!r}")

    # Ensure the final URL is absolute.
    if not full_url.startswith(f"{parsed_cdn.scheme}://"):
        raise ValueError("Failed to construct an absolute URL")

    return full_url