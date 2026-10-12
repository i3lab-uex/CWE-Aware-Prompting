import urllib.parse

# Predefined set of safe CDN domains (example)
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "static.cdn.net",
    "assets.safe-cdn.org"
}


def generate_external_resource_url(cdn_base: str, res_id: str, res_type: str) -> str:
    """
    Construct a fully qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base : str
        Base URL of the CDN (e.g. "https://cdn.example.com").
    res_id : str
        Identifier for the specific resource (e.g. "12345").
    res_type : str
        Type of resource, such as 'image', 'script', etc.

    Returns
    -------
    str
        A fully constructed, safe URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the CDN domain is not in ALLOWED_CDN_DOMAINS.
    """
    # Parse the base URL to validate and extract components
    parsed_base = urllib.parse.urlparse(cdn_base)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_base}")

    # Ensure the domain is allowed
    if parsed_base.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Domain '{parsed_base.hostname}' is not an allowed CDN domain."
        )

    # Normalise path to avoid double slashes
    base_path = parsed_base.path.rstrip("/")
    resource_path = f"{res_type}s/{urllib.parse.quote(res_id)}"
    full_path = f"/{base_path.lstrip('/')}/{resource_path}".replace("//", "/")

    # Reconstruct the full URL
    url_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        "",  # query
        ""   # fragment
    )
    return urllib.parse.urlunparse(url_parts)