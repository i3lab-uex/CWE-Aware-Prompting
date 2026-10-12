import urllib.parse

# Predefined set of domains considered safe CDN hosts.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.contentprovider.org",
}

def generate_external_resource_link(cdn_host_url: str,
                                    resource_tag: str,
                                    resource_category: str) -> str:
    """
    Build a secure URL for an external resource served from a CDN.

    Parameters
    ----------
    cdn_host_url : str
        Base URL of the CDN (e.g. "https://cdn.example.com").
    resource_tag : str
        Unique identifier for the specific resource (e.g. "logo.png").
    resource_category : str
        Category of the resource, typically a sub‑path such as "image" or "script".

    Returns
    -------
    str
        Fully qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to a host in :data:`ALLOWED_CDN_DOMAINS`.
    """
    if not cdn_host_url:
        raise ValueError("cdn_host_url must be a non-empty string")
    if not resource_tag:
        raise ValueError("resource_tag must be a non-empty string")
    if not resource_category:
        raise ValueError("resource_category must be a non-empty string")

    # Ensure the base URL ends with a single slash for consistent joining.
    base = cdn_host_url.rstrip('/') + '/'

    # Construct the relative path: e.g. "image/logo.png"
    relative_path = urllib.parse.quote(
        f"{resource_category.strip('/')}/{resource_tag.lstrip('/')}",
        safe="",
    )

    # Build the full URL.
    full_url = urllib.parse.urljoin(base, relative_path)

    # Validate that the host is an allowed CDN domain.
    parsed = urllib.parse.urlparse(full_url)
    host = parsed.hostname
    if not host or host.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN host: {host!r}")

    return full_url