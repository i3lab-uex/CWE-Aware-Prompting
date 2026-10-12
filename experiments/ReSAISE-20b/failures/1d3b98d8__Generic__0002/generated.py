import urllib.parse

# Example list of allowed CDN domains – replace with the real set in production.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.othercdn.org"
}


def build_cdn_resource_url(cdn_url: str, resource_identifier: str, resource_kind: str) -> str:
    """
    Construct a fully‑qualified CDN URL for the given resource.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN (e.g. "https://cdn.example.com").
    resource_identifier : str
        Unique identifier for the requested resource.
    resource_kind : str
        Kind of resource – typically "image", "script", etc.

    Returns
    -------
    str
        A fully‑qualified URL pointing to the resource on the CDN.

    Raises
    ------
    ValueError
        If the resulting URL does not belong to an allowed CDN domain or if
        the base URL is malformed.
    """
    # Parse and normalise the base CDN URL
    parsed_base = urllib.parse.urlparse(cdn_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_url!r}")

    # Ensure the domain is allowed
    if parsed_base.netloc.lower() not in {d.lower() for d in ALLOWED_CDN_DOMAINS}:
        raise ValueError(f"CDN domain {parsed_base.netloc!r} is not in the allowed list")

    # Safely encode path components
    safe_kind = urllib.parse.quote(resource_kind.strip("/"), safe="")
    safe_id = urllib.parse.quote(resource_identifier.strip("/"), safe="")

    # Build the full path
    base_path = parsed_base.path.rstrip("/")
    resource_path = urllib.parse.urljoin(base_path + "/", f"{safe_kind}/{safe_id}")

    # Reconstruct the URL
    final_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        resource_path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return final_url