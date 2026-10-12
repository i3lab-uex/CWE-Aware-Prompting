import urllib.parse
from typing import Set

# A set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.anothercdn.net",
    "static.myapp.org",
}

def _normalize_cdn_url(cdn_host_url: str) -> urllib.parse.ParseResult:
    """
    Normalises the CDN host URL, ensuring it has a scheme and returns a ParseResult.
    """
    parsed = urllib.parse.urlparse(cdn_host_url)
    if not parsed.scheme:
        # Default to https if no scheme is provided.
        parsed = urllib.parse.urlparse(f"https://{cdn_host_url}")
    return parsed

def generate_external_resource_link(
    cdn_host_url: str,
    resource_tag: str,
    resource_category: str
) -> str:
    """
    Build a full URL to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_host_url : str
        Base URL of the CDN (may or may not include a scheme).
    resource_tag : str
        Unique identifier for the resource (e.g., filename or hash).
    resource_category : str
        Category of the resource, such as 'image' or 'script'.

    Returns
    -------
    str
        The fully-qualified URL to the requested resource.

    Raises
    ------
    ValueError
        If the constructed URL does not belong to an allowed CDN domain.
    """
    # Normalise and parse the base CDN URL
    parsed_base = _normalize_cdn_url(cdn_host_url)

    # Validate the CDN domain
    if parsed_base.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"CDN domain '{parsed_base.hostname}' is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_CDN_DOMAINS)}"
        )

    # Build the path safely using urllib.parse.urljoin
    # Ensure we do not accidentally inject query parameters or fragments.
    safe_path = urllib.parse.quote_plus(resource_tag)
    # Construct the relative path: /{category}/{tag}
    relative_path = f"/{urllib.parse.quote_plus(resource_category)}/{safe_path}"

    full_url = urllib.parse.urljoin(
        f"{parsed_base.scheme}://{parsed_base.netloc}",
        relative_path
    )

    # Final sanity check: ensure the result still uses an allowed domain.
    final_parsed = urllib.parse.urlparse(full_url)
    if final_parsed.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Constructed URL points to disallowed domain '{final_parsed.hostname}'."
        )

    return full_url