import urllib.parse

# A set of CDN domains that are considered safe to use.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.somecdn.org",
}

def build_cdn_resource_url(cdn_url: str, resource_identifier: str, resource_kind: str) -> str:
    """
    Build a full CDN URL for a given resource.

    Parameters
    ----------
    cdn_url : str
        Base CDN URL (e.g. "https://cdn.example.com/").
    resource_identifier : str
        Unique identifier for the resource (e.g. "logo.png" or "app.min.js").
    resource_kind : str
        Kind of the resource (e.g. "image", "script").

    Returns
    -------
    str
        Fully qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If `cdn_url` does not belong to an allowed CDN domain or if any argument is invalid.
    """
    # Basic sanity checks
    if not all(isinstance(arg, str) and arg for arg in (cdn_url, resource_identifier, resource_kind)):
        raise ValueError("All arguments must be non‑empty strings.")

    # Parse the CDN base URL and verify its domain
    parsed_cdn = urllib.parse.urlparse(cdn_url)
    if not parsed_cdn.scheme or not parsed_cdn.netloc:
        raise ValueError(f"Invalid CDN URL: {cdn_url!r}")

    # Ensure the host is in the allowed set (case‑insensitive)
    cdn_host = parsed_cdn.hostname.lower()
    if cdn_host not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"CDN domain '{cdn_host}' is not allowed.")

    # Construct the path: /{resource_kind}/{resource_identifier}
    # Use quote to escape any unsafe characters in the identifier
    safe_identifier = urllib.parse.quote(resource_identifier, safe="")
    path_parts = [resource_kind.strip("/"), safe_identifier]
    resource_path = "/" + "/".join(path_parts)

    # Join the base URL with the new path
    full_url = urllib.parse.urljoin(cdn_url, resource_path)

    # Final validation: the resulting URL must still resolve to the same host
    final_parsed = urllib.parse.urlparse(full_url)
    if final_parsed.hostname.lower() != cdn_host:
        raise ValueError("Constructed URL points to a disallowed domain.")

    return full_url