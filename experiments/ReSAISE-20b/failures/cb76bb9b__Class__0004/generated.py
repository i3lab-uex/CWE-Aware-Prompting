import urllib.parse

# Example allowed CDN domains; in a real system this would be defined elsewhere.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.securecdn.org",
    "static.mysite.net",
}


def create_resource_url(base_cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Construct a fully-qualified URL for a resource hosted on a CDN.

    Parameters
    ----------
    base_cdn_url : str
        The base URL of the CDN, e.g. "https://cdn.example.com".
    res_id : str
        Unique identifier of the resource (typically a file name or hash).
    res_type : str
        Type/category of the resource, e.g. "image" or "script".

    Returns
    -------
    str
        The full URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the constructed URL does not belong to an allowed CDN domain.
    """
    # Parse the base URL and ensure it has a scheme and network location
    parsed_base = urllib.parse.urlparse(base_cdn_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("base_cdn_url must be a valid absolute URL")

    # Validate that the base CDN domain is allowed
    if parsed_base.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.hostname}' is not an allowed CDN")

    # Build the path component safely
    # Avoid leading/trailing slashes that could cause double separators
    res_type_clean = res_type.strip("/")
    res_id_clean = res_id.strip("/")
    path_parts = [res_type_clean, res_id_clean]
    relative_path = "/".join(part for part in path_parts if part)

    # Construct the final URL
    full_url = urllib.parse.urljoin(base_cdn_url.rstrip("/") + "/", relative_path)

    # Final sanity check: ensure the final URL still resolves to an allowed domain
    parsed_full = urllib.parse.urlparse(full_url)
    if parsed_full.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError("Constructed URL points to an unauthorized domain")

    return full_url