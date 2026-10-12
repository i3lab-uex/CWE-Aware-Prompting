import urllib.parse

# Define a set of approved CDN domains.  In real code this would be
# populated from configuration or environment variables.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.cdnservice.org",
}

def generate_cdn_content_url(
    cdn_origin_url: str,
    content_id: str,
    content_kind: str,
) -> str:
    """
    Build a fully‑qualified CDN URL for the requested content.

    Parameters
    ----------
    cdn_origin_url : str
        The base URL of the CDN, e.g. "https://cdn.example.com".
    content_id : str
        Unique identifier for the requested resource.
    content_kind : str
        The type of resource, e.g. "image", "script".

    Returns
    -------
    str
        A validated, absolute URL pointing to the resource.

    Raises
    ------
    ValueError
        If the resolved CDN domain is not in ``ALLOWED_CDN_DOMAINS``.
    """
    # Parse the origin URL and ensure it has a scheme and netloc
    parsed_origin = urllib.parse.urlparse(cdn_origin_url)
    if not parsed_origin.scheme or not parsed_origin.netloc:
        raise ValueError(f"Invalid CDN origin URL: {cdn_origin_url!r}")

    # Normalise the domain to lowercase for comparison
    origin_domain = parsed_origin.netloc.lower()
    if origin_domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Unauthorized CDN domain: {origin_domain!r}")

    # Construct the relative path.  ``/`` separators are normalized
    # by urljoin, so we simply join the kind and id.
    relative_path = urllib.parse.urljoin(
        f"/{content_kind.strip('/')}/",
        content_id.lstrip("/")
    )

    # Rebuild the full URL, preserving scheme and any existing path/query/fragment
    full_url = urllib.parse.urlunparse((
        parsed_origin.scheme,
        parsed_origin.netloc,
        relative_path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    # Final safety check: ensure the resulting domain is still allowed
    final_domain = urllib.parse.urlparse(full_url).netloc.lower()
    if final_domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Constructed URL points to an unauthorized domain: {final_domain!r}")

    return full_url