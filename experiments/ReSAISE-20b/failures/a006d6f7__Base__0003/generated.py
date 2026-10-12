import urllib.parse

# Example list of allowed CDN domains.  Replace or extend as needed.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "static.example.org",
    "assets.myapp.net"
}

def generate_cdn_content_url(cdn_origin_url: str, content_id: str, content_kind: str) -> str:
    """
    Assemble a secure CDN URL for the requested resource.

    Parameters
    ----------
    cdn_origin_url : str
        The base URL of the CDN (e.g. "https://cdn.example.com").
    content_id : str
        A unique identifier for the resource (e.g. "12345").
    content_kind : str
        The type of resource, e.g. 'image', 'script', etc.

    Returns
    -------
    str
        The fully qualified, validated URL pointing to the resource on the CDN.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain not in ALLOWED_CDN_DOMAINS.
    """
    # Basic type validation
    if not all(isinstance(arg, str) for arg in (cdn_origin_url, content_id, content_kind)):
        raise TypeError("All arguments must be strings")

    # Normalise the origin URL to ensure it ends with a slash
    base_url = cdn_origin_url.rstrip("/") + "/"

    # Build the relative path safely; quote components to avoid injection
    safe_kind = urllib.parse.quote(content_kind.strip("/"))
    safe_id = urllib.parse.quote(content_id.strip("/"))
    relative_path = f"{safe_kind}/{safe_id}"

    # Construct the full URL
    full_url = urllib.parse.urljoin(base_url, relative_path)

    # Parse the resulting URL to extract the netloc (domain)
    parsed = urllib.parse.urlparse(full_url)
    domain = parsed.netloc

    # Ensure the domain is in the allowed list
    if domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Unauthorized CDN domain: {domain}")

    return full_url