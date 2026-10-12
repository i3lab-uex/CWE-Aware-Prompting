import urllib.parse

# List of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net",
}

def create_external_resource_link(cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Construct a fully-qualified URL for an external resource located on a CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN.  Must include scheme (http or https).
    res_id : str
        Unique identifier for the resource.
    res_type : str
        Resource type, e.g. "image", "script", etc.

    Returns
    -------
    str
        The absolute URL pointing to the resource on the CDN.

    Raises
    ------
    ValueError
        If the resolved URL does not resolve to an allowed CDN domain,
        or if the input contains an unsupported scheme.
    """
    # Validate scheme
    parsed_base = urllib.parse.urlparse(cdn_url)
    if parsed_base.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed_base.scheme}")

    # Construct a path that is safe and predictable.
    # Use URL encoding for the resource id to avoid injection.
    encoded_id = urllib.parse.quote(res_id, safe='')
    path = f"/{res_type}/{encoded_id}"

    # Join the base URL and path.  urljoin ensures correct handling of slashes.
    full_url = urllib.parse.urljoin(cdn_url.rstrip('/') + '/', path.lstrip('/'))

    # Resolve the final URL's netloc to confirm it matches an allowed domain.
    parsed_full = urllib.parse.urlparse(full_url)
    if parsed_full.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {parsed_full.netloc}")

    return full_url