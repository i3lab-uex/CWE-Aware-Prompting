import urllib.parse

# Allowed CDN domains – update as required for your environment
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "static.myapp.net",
    "assets.somecdn.org",
}

def create_external_resource_link(cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Build a validated URL to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN (e.g. "https://cdn.example.com").
    res_id : str
        Unique identifier for the resource (e.g. "12345abc").
    res_type : str
        Type of resource – used as a path component (e.g. "image", "script").

    Returns
    -------
    str
        Fully-qualified, validated URL for the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in ``ALLOWED_CDN_DOMAINS``.
    """
    # Ensure components are safe for URL paths
    res_type_enc = urllib.parse.quote(res_type.strip("/"))
    res_id_enc   = urllib.parse.quote(res_id.strip("/"))

    # Construct the raw URL
    base_parsed = urllib.parse.urlparse(cdn_url.rstrip("/"))
    # Build the path: <base_path>/<res_type>/<res_id>
    new_path = urllib.parse.urljoin(base_parsed.path + "/", f"{res_type_enc}/{res_id_enc}")

    # Reassemble the URL
    full_url = urllib.parse.urlunparse((
        base_parsed.scheme,
        base_parsed.netloc,
        new_path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    # Validate domain against the whitelist
    if base_parsed.netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Unauthorized CDN domain: {base_parsed.netloc}")

    return full_url