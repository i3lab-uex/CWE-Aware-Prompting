import urllib.parse

# A whitelist of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "static.myapp.org",
    "assets.s3.amazonaws.com",
}

def generate_cdn_content_url(cdn_origin_url: str, content_id: str, content_kind: str) -> str:
    """
    Assemble a full CDN URL for the requested resource.

    Parameters
    ----------
    cdn_origin_url : str
        The base CDN URL, e.g. "https://cdn.example.com".
    content_id : str
        A unique identifier for the resource.
    content_kind : str
        The type of resource, e.g. "image" or "script".

    Returns
    -------
    str
        The fully-qualified, validated URL.

    Raises
    ------
    ValueError
        If the resolved CDN domain is not in ALLOWED_CDN_DOMAINS.
    """
    # Normalise the origin URL: ensure it has a scheme and no trailing slash
    parsed_origin = urllib.parse.urlparse(cdn_origin_url)
    if not parsed_origin.scheme:
        raise ValueError(f"Origin URL must include a scheme: {cdn_origin_url}")

    # Build the path to the resource
    # Example pattern: /{content_kind}/{content_id}
    resource_path = urllib.parse.urljoin(
        parsed_origin.path + "/", f"{content_kind}/{content_id}"
    )

    # Reconstruct the full URL
    full_url = urllib.parse.urlunparse((
        parsed_origin.scheme,
        parsed_origin.netloc,
        resource_path,
        '',  # params
        '',  # query
        ''   # fragment
    ))

    # Validate the domain against the whitelist
    netloc = urllib.parse.urlparse(full_url).netloc.lower()
    # Handle possible port numbers by stripping them
    host = netloc.split(':')[0]
    if host not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Unauthorized CDN domain: {host}")

    return full_url