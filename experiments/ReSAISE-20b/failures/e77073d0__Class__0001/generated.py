import urllib.parse

# Allowed CDN domains (example values – adjust as needed)
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.cdn.net",
}

def build_cdn_resource_url(cdn_url_base: str, file_id: str, file_type: str) -> str:
    """
    Construct a fully-qualified CDN URL for a given resource.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN, e.g. "https://cdn.example.com".
    file_id : str
        Unique identifier for the resource (e.g. a hash or UUID).
    file_type : str
        Type of resource, used to build the path (e.g. "image", "script").

    Returns
    -------
    str
        A fully-qualified, validated URL pointing to the resource.

    Raises
    ------
    ValueError
        If the resolved domain is not in ``ALLOWED_CDN_DOMAINS`` or if any
        component cannot be safely encoded.
    """
    # Ensure the base URL has a scheme; default to https if missing
    parsed_base = urllib.parse.urlparse(cdn_url_base)
    if not parsed_base.scheme:
        parsed_base = parsed_base._replace(scheme="https")

    # Validate the domain
    netloc = parsed_base.netloc.lower()
    if not any(netloc == allowed or netloc.endswith("." + allowed) for allowed in ALLOWED_CDN_DOMAINS):
        raise ValueError(f"Unauthorized CDN domain: {netloc}")

    # Encode path components to prevent injection or traversal
    safe_file_type = urllib.parse.quote(file_type.strip(), safe="")
    safe_file_id = urllib.parse.quote(file_id.strip(), safe="")

    # Build the relative path: /{file_type}/{file_id}
    relative_path = f"/{safe_file_type}/{safe_file_id}"

    # Combine base URL with the relative path
    full_url = urllib.parse.urljoin(parsed_base.geturl(), relative_path)

    # Final sanity check: parse again and ensure scheme + domain are still valid
    final_parsed = urllib.parse.urlparse(full_url)
    if not (final_parsed.scheme in ("http", "https") and final_parsed.netloc.lower() == netloc):
        raise ValueError(f"Malformed URL after construction: {full_url}")

    return full_url