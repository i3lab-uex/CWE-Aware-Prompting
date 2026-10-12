import urllib.parse

# Allowed CDN domains (example list – extend as needed)
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net",
}

def generate_cdn_content_url(cdn_origin_url: str, content_id: str, content_kind: str) -> str:
    """
    Assemble a fully qualified URL for a resource hosted on an external CDN.

    Parameters
    ----------
    cdn_origin_url : str
        Base URL of the CDN, e.g. "https://cdn.example.com".
    content_id : str
        Unique identifier for the requested resource.
    content_kind : str
        Type of resource (e.g. "image", "script").

    Returns
    -------
    str
        A validated, fully qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the CDN domain is not in :data:`ALLOWED_CDN_DOMAINS` or if any
        component contains suspicious characters that could lead to path traversal.
    """
    # ---------- 1. Validate the base URL ----------
    parsed_origin = urllib.parse.urlparse(cdn_origin_url)
    if not parsed_origin.scheme or not parsed_origin.netloc:
        raise ValueError(f"Invalid CDN origin URL: {cdn_origin_url!r}")

    # Normalise the domain for comparison
    cdn_domain = parsed_origin.netloc.lower()
    if cdn_domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Unauthorized CDN domain: {cdn_domain!r}")

    # ---------- 2. Sanitize path components ----------
    def _sanitize(component: str) -> str:
        if not component or any(c in component for c in ("..", "/", "\\", "%")):
            raise ValueError(f"Invalid path component: {component!r}")
        return urllib.parse.quote(component, safe="")

    kind = _sanitize(content_kind)
    cid = _sanitize(content_id)

    # ---------- 3. Build the full URL ----------
    # Ensure the base ends with a slash to avoid accidental concatenation
    base = cdn_origin_url.rstrip("/") + "/"
    path = f"{kind}/{cid}"
    full_url = urllib.parse.urljoin(base, path)

    # Final sanity check: ensure the resulting URL uses an allowed domain
    final_parsed = urllib.parse.urlparse(full_url)
    if final_parsed.netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Constructed URL points to unauthorized domain: {full_url!r}")

    return full_url