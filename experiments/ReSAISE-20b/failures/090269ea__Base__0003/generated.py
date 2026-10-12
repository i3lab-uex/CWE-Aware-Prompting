import urllib.parse

# Set of CDN domains that are considered safe. Adjust as necessary.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "static.myapp.org",
    "assets.global-cdn.net"
}

def create_external_resource_link(cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Build a fully-qualified URL pointing to an external resource on a CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN. Must contain scheme and domain only.
    res_id : str
        Unique identifier for the resource (e.g., image hash or script name).
    res_type : str
        Type of the resource (e.g., 'image', 'script'). Will be used as a path segment.

    Returns
    -------
    str
        Fully-qualified URL that can be safely used to fetch the resource.

    Raises
    ------
    ValueError
        If `cdn_url` resolves to a domain not present in ``ALLOWED_CDN_DOMAINS`` or
        if the constructed URL points to an unauthorized domain.
    """
    # Parse the CDN base URL
    parsed_cdn = urllib.parse.urlparse(cdn_url)

    # Validate scheme
    if parsed_cdn.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed_cdn.scheme}")

    # Validate domain
    hostname = parsed_cdn.hostname
    if not hostname or hostname.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"CDN domain '{hostname}' is not allowed")

    # Normalize resource type and ID
    res_type_clean = urllib.parse.quote(res_type.strip().lstrip("/"))
    res_id_clean = urllib.parse.quote(res_id.strip().lstrip("/"))

    # Construct the path: /{res_type}/{res_id}
    path = urllib.parse.urljoin("/", f"{res_type_clean}/{res_id_clean}")

    # Build the final URL, preserving query and fragment from base if any
    final_url = urllib.parse.urlunparse((
        parsed_cdn.scheme,
        parsed_cdn.netloc,
        path,
        "",          # params
        "",          # query
        ""           # fragment
    ))

    # Final sanity check: ensure the domain hasn't changed after building
    final_parsed = urllib.parse.urlparse(final_url)
    if final_parsed.hostname.lower() != hostname.lower():
        raise ValueError("URL construction altered the CDN domain")

    return final_url