import urllib.parse

# Predefined set of allowed CDN domains (example entries)
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.somesite.org",
    "static.myapp.net",
}

def generate_external_resource_url(cdn_base: str, res_id: str, res_type: str) -> str:
    """
    Construct a fully qualified URL pointing to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base : str
        Base URL of the Content Delivery Network (e.g. "https://cdn.example.com").
    res_id : str
        Identifier of the resource to retrieve (e.g. "images/logo.png").
    res_type : str
        Type of the resource, used to prepend a sub‑path (e.g. "image", "script").

    Returns
    -------
    str
        The fully constructed URL.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in ``ALLOWED_CDN_DOMAINS``.
    """
    # Ensure the base URL uses HTTPS for security
    parsed_base = urllib.parse.urlparse(cdn_base)
    if not parsed_base.scheme:
        raise ValueError("cdn_base must include a scheme (e.g., https://)")
    if parsed_base.scheme not in {"http", "https"}:
        raise ValueError("cdn_base must use http or https scheme")

    # Build the path: e.g., "/image/<res_id>"
    resource_path = urllib.parse.urljoin(f"/{res_type}/", res_id)

    # Construct the full URL
    full_url = urllib.parse.urljoin(cdn_base.rstrip("/") + "/", resource_path.lstrip("/"))

    # Validate that the hostname is in the allowed list
    host = urllib.parse.urlparse(full_url).hostname
    if not host or host.lower() not in {d.lower() for d in ALLOWED_CDN_DOMAINS}:
        raise ValueError(f"Disallowed CDN domain: {host}")

    return full_url