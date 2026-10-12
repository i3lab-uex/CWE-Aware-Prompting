import urllib.parse
from typing import Set

# Example set of allowed CDN domains.  In real code this would be
# configured elsewhere and imported.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net",
}

def generate_external_resource_link(
    cdn_host_url: str,
    resource_tag: str,
    resource_category: str,
) -> str:
    """
    Build a full URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_host_url : str
        The base URL of the CDN, e.g. "https://cdn.example.com".
    resource_tag : str
        The unique identifier for the resource, e.g. "logo.png".
    resource_category : str
        The category of the resource (e.g. 'image', 'script').

    Returns
    -------
    str
        A fully-qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL is not served from an allowed CDN domain.
    """
    # Ensure we have a valid scheme; default to https if missing
    parsed = urllib.parse.urlparse(cdn_host_url)
    scheme = parsed.scheme or "https"
    netloc = parsed.netloc

    if not netloc:
        # Handle case where user omitted scheme, e.g. "cdn.example.com"
        netloc = parsed.path
    if not netloc:
        raise ValueError("cdn_host_url must contain a domain")

    # Normalise the netloc: lower‑case, strip port if present
    host = netloc.split(":")[0].lower()

    # Validate domain against the allowed set
    if host not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{host}' is not an allowed CDN")

    # Build the path.  Ensure it starts with a slash and avoid double slashes.
    category_path = f"/{resource_category.strip('/')}"
    resource_path = f"{category_path}/{resource_tag.lstrip('/')}"

    # Re‑assemble the URL
    full_url = urllib.parse.urlunparse(
        (
            scheme,
            netloc,
            resource_path,
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return full_url