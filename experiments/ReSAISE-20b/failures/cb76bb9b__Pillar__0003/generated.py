import urllib.parse

# Example set of allowed CDN domains.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.mydomain.org",
    "static.myapp.net",
}

def create_resource_url(base_cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Build a full URL for a resource hosted on a CDN.

    Parameters
    ----------
    base_cdn_url : str
        Base URL of the CDN, e.g. "https://cdn.example.com".
    res_id : str
        Unique identifier of the resource.
    res_type : str
        Type/category of the resource, e.g. "image" or "script".

    Returns
    -------
    str
        The fully-qualified URL pointing to the resource.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to a domain in
        ``ALLOWED_CDN_DOMAINS``.
    """
    # Normalise the base URL to ensure it ends with a slash
    if not base_cdn_url.endswith("/"):
        base_cdn_url += "/"

    # Prevent path traversal and other injection attacks by percent-encoding
    safe_res_id = urllib.parse.quote(res_id, safe="")
    safe_res_type = urllib.parse.quote(res_type, safe="")

    # Construct the relative path
    relative_path = f"{safe_res_type}/{safe_res_id}"

    # Join the base URL with the relative path
    full_url = urllib.parse.urljoin(base_cdn_url, relative_path)

    # Parse the resulting URL to extract its domain
    parsed = urllib.parse.urlparse(full_url)
    hostname = parsed.hostname

    # Validate that the hostname is in the allowed set
    if not hostname or hostname.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Constructed URL '{full_url}' uses disallowed CDN domain: {hostname}"
        )

    return full_url