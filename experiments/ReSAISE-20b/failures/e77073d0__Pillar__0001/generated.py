import urllib.parse

# A set of CDN domains that are considered safe for use.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "static.example.org",
    "assets.myapp.net",
}

def build_cdn_resource_url(cdn_url_base: str, file_id: str, file_type: str) -> str:
    """
    Construct a fully-qualified URL to fetch a resource from an external CDN.

    Parameters
    ----------
    cdn_url_base : str
        The base URL of the CDN (e.g. "https://cdn.example.com/").
    file_id : str
        A unique identifier for the resource (e.g. a hash or UUID).
    file_type : str
        The type of the resource, used to determine the path component
        (e.g. "image", "script").

    Returns
    -------
    str
        The fully-qualified, validated URL for the requested resource.

    Raises
    ------
    ValueError
        If the resolved CDN domain is not in ``ALLOWED_CDN_DOMAINS``.
    """
    # Normalise the base URL so it ends with a slash
    if not cdn_url_base.endswith("/"):
        cdn_url_base += "/"

    # Build the relative path for the resource
    relative_path = urllib.parse.urljoin(f"{file_type}/", file_id)

    # Resolve the full URL
    full_url = urllib.parse.urljoin(cdn_url_base, relative_path)

    # Parse the URL to inspect its components
    parsed = urllib.parse.urlparse(full_url)

    # Ensure we have a scheme and netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {full_url}")

    # Validate the domain
    if parsed.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Unauthorized CDN domain '{parsed.netloc}'. "
            f"Allowed domains: {', '.join(sorted(ALLOWED_CDN_DOMAINS))}"
        )

    # Return the fully-qualified URL
    return full_url