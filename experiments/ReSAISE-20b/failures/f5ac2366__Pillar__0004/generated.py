import urllib.parse
from typing import Set

# Define the set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.content.org",
}

def construct_external_resource_url(
    cdn_base_url: str,
    resource_id: str,
    resource_type: str,
) -> str:
    """
    Construct a fully‑qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base_url : str
        The base URL of the CDN (e.g. "https://cdn.example.com").
    resource_id : str
        The identifier of the resource (e.g. a file name or hash).
    resource_type : str
        The type of the resource, used as a sub‑directory in the URL path
        (e.g. "image", "script").

    Returns
    -------
    str
        The fully resolved URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the constructed URL does not point to an allowed CDN domain or if
        any component is invalid.
    """
    # 1. Parse the base URL and validate it
    parsed_base = urllib.parse.urlparse(cdn_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_base_url!r}")

    # 2. Ensure the domain is allowed
    if parsed_base.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {parsed_base.hostname!r}")

    # 3. Clean the resource type and ID to avoid path traversal
    safe_resource_type = urllib.parse.quote(resource_type.strip("/"), safe="")
    safe_resource_id = urllib.parse.quote(resource_id.strip("/"), safe="")

    # 4. Build the new path by appending the type and ID
    base_path = parsed_base.path.rstrip("/")
    new_path = urllib.parse.urljoin(f"{base_path}/", f"{safe_resource_type}/{safe_resource_id}")

    # 5. Reconstruct the full URL
    final_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        new_path,
        "",  # params
        "",  # query
        "",  # fragment
    ))

    # Final safety check: re‑parse to confirm the hostname is still allowed
    final_parsed = urllib.parse.urlparse(final_url)
    if final_parsed.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Constructed URL points to disallowed domain: {final_parsed.hostname!r}")

    return final_url