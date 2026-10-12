import urllib.parse

# Example set of allowed CDN domains. In a real application this should be
# populated with the actual CDNs that are trusted.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.somecdn.org",
}

def build_cdn_resource_url(cdn_url: str, resource_identifier: str, resource_kind: str) -> str:
    """
    Construct a full URL for a CDN-hosted resource.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN. Must belong to one of the `ALLOWED_CDN_DOMAINS`.
    resource_identifier : str
        Unique identifier for the requested resource (e.g. file name or hash).
    resource_kind : str
        Type of the resource, e.g., 'image', 'script', etc.

    Returns
    -------
    str
        The fully-qualified URL pointing to the requested resource on the CDN.

    Raises
    ------
    ValueError
        If `cdn_url` does not resolve to an allowed CDN domain, or if the final URL
        points outside of that domain (e.g. due to a relative path that escapes the base).
    """
    # Parse the CDN base URL and validate its domain.
    parsed_base = urllib.parse.urlparse(cdn_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid CDN base URL: missing scheme or netloc")

    # Normalize the domain for comparison (case-insensitive, ignore port)
    base_domain = parsed_base.hostname.lower()
    if base_domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"CDN domain '{base_domain}' is not in the list of allowed domains")

    # Build a safe relative path. We strip any leading/trailing slashes to avoid
    # double slashes or attempts to escape the base path.
    safe_resource_kind = resource_kind.strip("/")
    safe_identifier = resource_identifier.strip("/")

    # Construct the relative path: <resource_kind>/<identifier>
    rel_path = urllib.parse.urljoin("/", f"{safe_resource_kind}/{safe_identifier}")

    # Join the base URL with the relative path.
    full_url = urllib.parse.urljoin(cdn_url.rstrip("/") + "/", rel_path.lstrip("/"))

    # Parse the resulting URL and confirm it still points to an allowed domain.
    parsed_full = urllib.parse.urlparse(full_url)
    final_domain = parsed_full.hostname.lower()
    if final_domain != base_domain:
        raise ValueError("Resulting URL points to a different domain than the CDN base")

    return full_url