import urllib.parse

# Example of allowed CDN domains – replace with the real set used in your project.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net",
}

def build_external_resource_link(cdn_url: str, resource_key: str, res_category: str) -> str:
    """
    Construct a fully qualified URL pointing to an external resource on a CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN (must be an absolute URL with scheme).
    resource_key : str
        Identifier for the specific resource (e.g., filename or hash).
    res_category : str
        Category/type of the resource (e.g., 'image', 'script').

    Returns
    -------
    str
        The absolute URL to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL does not target a domain listed in ALLOWED_CDN_DOMAINS,
        or if the base URL is not absolute.
    """
    # Parse the CDN base URL to validate it
    parsed_cdn = urllib.parse.urlparse(cdn_url)
    if not parsed_cdn.scheme or not parsed_cdn.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_url!r}")

    # Ensure the domain is allowed
    if parsed_cdn.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"CDN domain {parsed_cdn.hostname!r} is not allowed")

    # Build the relative path for the resource
    # Use '/' as separator; strip any leading/trailing slashes to avoid double slashes.
    rel_path = f"/{res_category.strip('/')}/{resource_key.strip('/')}"
    
    # Construct the full URL
    full_url = urllib.parse.urljoin(cdn_url.rstrip('/') + '/', rel_path.lstrip('/'))

    # Final domain check (in case cdn_url had a trailing path that changed the host)
    final_parsed = urllib.parse.urlparse(full_url)
    if final_parsed.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Resulting URL points to disallowed domain: {final_parsed.hostname!r}")

    return full_url