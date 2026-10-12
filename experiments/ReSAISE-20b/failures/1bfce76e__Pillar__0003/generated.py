import urllib.parse

# A predefined set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "static.myapp.org",
    "assets.content.net",
}

def generate_external_resource_url(cdn_base: str, res_id: str, res_type: str) -> str:
    """
    Construct a full URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base : str
        Base URL of the CDN, e.g. "https://cdn.example.com/"
    res_id : str
        Identifier of the resource (path fragment). Should be URL‑safe.
    res_type : str
        Type of the resource (e.g., "image", "script").

    Returns
    -------
    str
        Fully resolved URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resolved URL resolves to a domain that is not in
        :data:`ALLOWED_CDN_DOMAINS`.
    """
    # Ensure the base URL is absolute and contains a scheme.
    parsed_base = urllib.parse.urlparse(cdn_base)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_base!r}")

    # Build the relative path and join it with the base.
    # ``res_type`` and ``res_id`` are joined using a slash to form the path.
    relative_path = urllib.parse.quote_plus(res_type.strip()) + "/" + urllib.parse.quote_plus(res_id.strip())
    full_url = urllib.parse.urljoin(cdn_base, relative_path)

    # Resolve the final URL and check its domain.
    parsed_full = urllib.parse.urlparse(full_url)
    domain = parsed_full.hostname

    if domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {domain!r}")

    return full_url