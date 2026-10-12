import urllib.parse

# Set of CDN domains considered safe (example entries)
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.contentprovider.org",
}

def create_resource_url(base_cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Construct a fully qualified URL for a resource hosted on an allowed CDN.

    Parameters
    ----------
    base_cdn_url : str
        Base URL of the CDN (e.g., 'https://cdn.example.com/').
    res_id : str
        Unique identifier for the resource (e.g., '12345').
    res_type : str
        Type of resource ('image', 'script', etc.).

    Returns
    -------
    str
        The complete URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to an allowed CDN domain or if
        the base URL has an unsupported scheme.
    """
    # Ensure base_cdn_url ends with a slash for proper joining
    if not base_cdn_url.endswith("/"):
        base_cdn_url += "/"

    # Build the relative path
    # We escape res_id and res_type to avoid injection via path traversal or other attacks
    safe_res_id = urllib.parse.quote(res_id, safe="")
    safe_res_type = urllib.parse.quote(res_type, safe="")

    relative_path = f"{safe_res_type}/{safe_res_id}"
    full_url = urllib.parse.urljoin(base_cdn_url, relative_path)

    # Parse the URL to validate components
    parsed = urllib.parse.urlparse(full_url)

    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Extract the hostname (may include port)
    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a valid hostname")

    # Strip port if present for domain comparison
    host_no_port = host.split(":")[0].lower()

    if host_no_port not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{host_no_port}' is not in the list of allowed CDN domains")

    return full_url