import urllib.parse

# A set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.content.org",
}

def generate_cdn_content_url(cdn_origin_url: str, content_id: str, content_kind: str) -> str:
    """
    Build a fully-qualified CDN URL for a given resource.

    Parameters
    ----------
    cdn_origin_url : str
        The base URL of the CDN (e.g. "https://cdn.example.com").
    content_id : str
        A unique identifier for the resource.
    content_kind : str
        The type of resource (e.g. "image", "script").

    Returns
    -------
    str
        The complete, validated URL pointing to the resource.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in ``ALLOWED_CDN_DOMAINS``.
    """
    # Ensure the origin URL is absolute and has a scheme
    parsed_origin = urllib.parse.urlparse(cdn_origin_url)
    if not parsed_origin.scheme or not parsed_origin.netloc:
        raise ValueError(f"Invalid CDN origin URL: {cdn_origin_url!r}")

    # Verify that the domain is allowed
    domain = parsed_origin.hostname.lower()
    if domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain {domain!r} is not an allowed CDN domain")

    # Construct the path: /{content_kind}/{content_id}
    # Use quote to ensure special characters are percent‑encoded
    safe_content_kind = urllib.parse.quote(content_kind.strip("/"), safe="")
    safe_content_id   = urllib.parse.quote(content_id.strip("/"), safe="")

    # Join the path to the origin, preserving any existing path in the origin
    full_path = urllib.parse.urljoin(parsed_origin.path + "/", f"{safe_content_kind}/{safe_content_id}")

    # Reconstruct the final URL
    final_url = urllib.parse.urlunparse((
        parsed_origin.scheme,
        parsed_origin.netloc,
        full_path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return final_url