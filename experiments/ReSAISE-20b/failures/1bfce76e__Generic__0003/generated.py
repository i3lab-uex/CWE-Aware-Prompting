import urllib.parse

# Predefined set of allowed CDN domains (example)
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "static.example.org",
    "assets.safe-cdn.net",
}

def generate_external_resource_url(cdn_base: str, res_id: str, res_type: str) -> str:
    """
    Construct a fully-qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base : str
        Base URL of the Content Delivery Network (e.g., "https://cdn.example.com").
    res_id : str
        Identifier of the resource to retrieve. Must be a relative path component without slashes or traversal.
    res_type : str
        Type of the resource (e.g., "image", "script").

    Returns
    -------
    str
        The fully constructed URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resolved URL does not target a domain in ``ALLOWED_CDN_DOMAINS`` or if
        the resource identifier contains unsafe characters.
    """
    # Validate and normalize cdn_base
    parsed_base = urllib.parse.urlparse(cdn_base)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_base!r}")

    # Ensure the CDN domain is allowed
    if parsed_base.netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"CDN domain '{parsed_base.netloc}' is not in the allowed list")

    # Sanitize resource identifier
    if any(c in res_id for c in ('/', '\\', '..')) or not res_id:
        raise ValueError(f"Invalid resource identifier: {res_id!r}")

    # URL‑encode the components to prevent injection or traversal
    safe_res_type = urllib.parse.quote(res_type.strip('/'), safe='')
    safe_res_id   = urllib.parse.quote(res_id.strip('/'), safe='')

    # Build the relative path and join with base
    rel_path = f"/{safe_res_type}/{safe_res_id}"
    full_url = urllib.parse.urljoin(parsed_base.geturl(), rel_path)

    # Final check: the resolved domain must still be allowed
    final_netloc = urllib.parse.urlparse(full_url).netloc.lower()
    if final_netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Resolved URL points to disallowed domain: {final_netloc}")

    return full_url