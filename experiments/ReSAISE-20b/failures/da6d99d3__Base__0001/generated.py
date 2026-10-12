import urllib.parse
from typing import Set

# Predefined set of safe CDN domains.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "static.content.net",
    "assets.myapp.org",
}

def build_external_resource_link(cdn_url: str, resource_key: str, res_category: str) -> str:
    """
    Construct a fully qualified URL pointing to an external resource.

    Parameters
    ----------
    cdn_url : str
        The base URL of the CDN. Must resolve to a domain in ``ALLOWED_CDN_DOMAINS``.
    resource_key : str
        Identifier of the requested resource (e.g., file name or path).
    res_category : str
        Category of the resource, used as a directory prefix (e.g., 'image', 'script').

    Returns
    -------
    str
        The absolute URL to the external resource.

    Raises
    ------
    ValueError
        If the resolved CDN domain is not in ``ALLOWED_CDN_DOMAINS``.
    """
    # Parse the CDN URL to extract scheme and network location
    parsed_cdn = urllib.parse.urlparse(cdn_url)

    # Reject URLs that don't have a scheme or netloc
    if not parsed_cdn.scheme or not parsed_cdn.netloc:
        raise ValueError(f"Invalid CDN URL: {cdn_url!r}")

    # Normalize the netloc (lowercase, strip any port if present)
    netloc = parsed_cdn.netloc.split(":")[0].lower()

    # Ensure the CDN domain is allowed
    if netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"CDN domain {netloc!r} is not allowed")

    # Build the path component safely:
    # - Ensure category and key are URL‑encoded to avoid injection or traversal.
    safe_category = urllib.parse.quote(res_category.strip("/"))
    safe_key = urllib.parse.quote(resource_key.strip("/"))

    # Construct the relative path: <category>/<resource_key>
    rel_path = f"{safe_category}/{safe_key}"

    # Combine the base CDN URL with the relative path
    full_url = urllib.parse.urljoin(cdn_url.rstrip("/") + "/", rel_path)

    # Final safety check: the resulting URL must still resolve to an allowed domain
    final_parsed = urllib.parse.urlparse(full_url)
    final_netloc = final_parsed.netloc.split(":")[0].lower()
    if final_netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Resulting URL {full_url!r} resolves to disallowed domain")

    return full_url