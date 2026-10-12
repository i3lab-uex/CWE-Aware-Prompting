import urllib.parse

# Set of CDN domains that are considered safe/allowed.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.mywebsite.org",
    "static.cdnprovider.net",
}

def generate_external_resource_link(cdn_host_url: str, resource_tag: str, resource_category: str) -> str:
    """
    Build a fully‑qualified URL to an external CDN resource.

    Parameters
    ----------
    cdn_host_url : str
        The base URL of the CDN (e.g., "https://cdn.example.com/").
    resource_tag : str
        Unique identifier for the requested resource.
    resource_category : str
        Category of the resource (e.g., "image", "script").

    Returns
    -------
    str
        The complete URL pointing to the resource.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain that is not in
        ``ALLOWED_CDN_DOMAINS``.
    """
    # Ensure the host URL ends with a slash for correct urljoin behaviour
    base_url = cdn_host_url.rstrip("/") + "/"

    # Construct a relative path. We normalise it to avoid double slashes.
    relative_path = urllib.parse.quote_plus(f"{resource_category.rstrip('/')}/{resource_tag.lstrip('/')}")
    full_url = urllib.parse.urljoin(base_url, relative_path)

    # Parse the resulting URL to extract its domain
    parsed = urllib.parse.urlparse(full_url)
    hostname = parsed.hostname

    if not hostname or hostname.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {hostname!r}")

    # Optional: enforce https scheme for security
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    return full_url