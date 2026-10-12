import urllib.parse
from typing import Set

# Example set of allowed CDN domains – replace with the actual ones in your project
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.content.org",
}

def build_cdn_resource_url(
    cdn_url: str,
    resource_identifier: str,
    resource_kind: str,
) -> str:
    """
    Construct a secure CDN URL for the requested resource.

    Parameters
    ----------
    cdn_url : str
        The base URL of the CDN (e.g., "https://cdn.example.com").
    resource_identifier : str
        The unique identifier for the resource (e.g., a file hash or name).
    resource_kind : str
        The kind of resource, e.g., "image" or "script".

    Returns
    -------
    str
        The fully-qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to a domain listed in
        ``ALLOWED_CDN_DOMAINS``.
    """
    # 1. Parse the base CDN URL
    parsed_base = urllib.parse.urlparse(cdn_url)
    if parsed_base.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed_base.scheme!r}")

    # 2. Ensure the domain is allowed
    if parsed_base.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain {parsed_base.hostname!r} is not an allowed CDN")

    # 3. Construct the path safely
    # Avoid any leading/trailing slashes that could lead to double slashes or path traversal.
    safe_kind = urllib.parse.quote(resource_kind.strip("/"))
    safe_id = urllib.parse.quote(resource_identifier.strip("/"))

    # Build the relative path: e.g., "/image/abcd1234.png"
    relative_path = f"/{safe_kind}/{safe_id}"

    # 4. Join the base URL with the relative path
    full_url = urllib.parse.urljoin(parsed_base.geturl(), relative_path)

    # 5. Final check: re-parse to ensure domain hasn't changed
    parsed_full = urllib.parse.urlparse(full_url)
    if parsed_full.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Constructed URL points to disallowed domain: {parsed_full.hostname!r}"
        )

    return full_url