import urllib.parse

# Example set of allowed CDN domains. In real code, import from config.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.safe-cdn.net"
}


def generate_external_resource_url(cdn_base: str, res_id: str, res_type: str) -> str:
    """
    Construct a full URL to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base : str
        Base URL of the CDN (e.g., "https://cdn.example.com").
    res_id : str
        Identifier of the resource (e.g., "12345.jpg").
    res_type : str
        Type/category of the resource (e.g., "image", "script").

    Returns
    -------
    str
        Fully-qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the CDN domain is not in ALLOWED_CDN_DOMAINS or if the constructed URL
        resolves to an untrusted domain.
    """
    # Parse and normalise the CDN base URL
    parsed_base = urllib.parse.urlparse(cdn_base)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid CDN base URL")

    # Ensure the domain is allowed
    if parsed_base.netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"CDN domain '{parsed_base.netloc}' is not allowed")

    # Sanitize inputs: prevent path traversal or scheme injection
    safe_res_type = urllib.parse.quote(res_type.strip('/'))
    safe_res_id = urllib.parse.quote(res_id.strip('/'))

    # Construct the relative path
    rel_path = f"/{safe_res_type}/{safe_res_id}"

    # Resolve the final URL
    full_url = urllib.parse.urljoin(cdn_base.rstrip('/') + '/', rel_path.lstrip('/'))

    # Double-check the final URL's domain
    final_parsed = urllib.parse.urlparse(full_url)
    if final_parsed.netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Resulting URL domain '{final_parsed.netloc}' is not allowed")

    return full_url