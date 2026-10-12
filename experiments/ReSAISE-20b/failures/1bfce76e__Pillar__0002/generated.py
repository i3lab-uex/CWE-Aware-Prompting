import urllib.parse

# Set of CDN domains that are considered safe.  These should be updated as needed.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.mysite.org",
}

def generate_external_resource_url(cdn_base: str, res_id: str, res_type: str) -> str:
    """
    Construct a fully‑qualified URL pointing to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base : str
        Base URL of the Content Delivery Network.  It may or may not end with a trailing slash.
    res_id : str
        Identifier for the requested resource (e.g., filename or hash).
    res_type : str
        Type of resource.  This value is used as a sub‑path under the CDN base
        (e.g., 'image', 'script').

    Returns
    -------
    str
        The complete URL that can be used to retrieve the resource.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to one of the allowed CDN domains.
    """
    # Normalise base URL: ensure it ends with a slash so that urljoin behaves predictably.
    if not cdn_base.endswith("/"):
        cdn_base = cdn_base + "/"

    # Build the relative path.  Avoid leading slashes to prevent overriding the base.
    rel_path = urllib.parse.quote_plus(res_type.strip("/") + "/" + res_id.strip("/"))

    # Construct the full URL
    full_url = urllib.parse.urljoin(cdn_base, rel_path)

    # Validate that the hostname is in the whitelist
    parsed = urllib.parse.urlparse(full_url)
    host = parsed.hostname

    if host is None or host.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {host!r}")

    return full_url