import urllib.parse

# Example set of allowed CDN domains – replace with the actual list for your project
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.provider.org",
}

def generate_external_resource_url(cdn_base: str, res_id: str, res_type: str) -> str:
    """
    Construct a fully qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base : str
        Base URL of the CDN (e.g. "https://cdn.example.com").
    res_id : str
        Identifier of the resource (e.g. "12345").
    res_type : str
        Type/category of the resource (e.g. "image", "script").

    Returns
    -------
    str
        The full URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the CDN domain is not in :data:`ALLOWED_CDN_DOMAINS` or if
        ``cdn_base`` is not a valid absolute URL.
    """
    # Parse the base URL
    parsed = urllib.parse.urlparse(cdn_base)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_base!r}")

    # Validate domain
    if parsed.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain {parsed.hostname!r} is not an allowed CDN")

    # Normalise path: ensure it ends with a slash
    base_path = parsed.path.rstrip("/") + "/"

    # Construct the resource path (e.g. /image/12345)
    res_path = urllib.parse.quote(f"{res_type}/{res_id}".lstrip("/"))

    # Build the full URL
    full_url = urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        urllib.parse.urljoin(base_path, res_path),
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return full_url