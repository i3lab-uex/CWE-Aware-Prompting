import urllib.parse

# Set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.cdn.net",
}

def create_external_resource_link(cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Construct a full URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN, e.g. "https://cdn.example.com".
    res_id : str
        Unique identifier for the resource (usually a hash or UUID).
    res_type : str
        Resource type, e.g. "image", "script".

    Returns
    -------
    str
        Fully-qualified, validated URL to the requested resource.

    Raises
    ------
    ValueError
        If the constructed URL points to a domain not in ``ALLOWED_CDN_DOMAINS``.
    """
    # Ensure cdn_url has a scheme; default to https if missing
    parsed_cdn = urllib.parse.urlparse(cdn_url)
    if not parsed_cdn.scheme:
        cdn_url = f"https://{cdn_url}"
        parsed_cdn = urllib.parse.urlparse(cdn_url)

    # Normalise the CDN path: make sure it ends with a slash
    base_path = parsed_cdn.path.rstrip("/") + "/"

    # Build the relative resource path
    rel_path = urllib.parse.quote(f"{res_type}/{res_id}")

    # Join base and relative path
    full_url = urllib.parse.urljoin(cdn_url.rstrip("/") + "/", rel_path)

    # Validate the domain
    final_parsed = urllib.parse.urlparse(full_url)
    if final_parsed.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Unauthorized CDN domain: {final_parsed.hostname!r}. "
            f"Allowed domains are: {sorted(ALLOWED_CDN_DOMAINS)}"
        )

    return full_url