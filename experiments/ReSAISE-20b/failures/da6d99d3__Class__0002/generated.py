import urllib.parse

# Example set of allowed CDN domains; in a real application this should be defined elsewhere
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.safe-cdn.org",
    "static.myapp.net",
}

def build_external_resource_link(cdn_url: str, resource_key: str, res_category: str) -> str:
    """
    Construct a fully-qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the Content Delivery Network.
    resource_key : str
        Identifier (e.g., filename or path) of the requested resource.
    res_category : str
        Category/type of the resource (e.g., 'image', 'script').

    Returns
    -------
    str
        The fully constructed URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resolved domain is not in :data:`ALLOWED_CDN_DOMAINS`.
    """
    # Parse the CDN URL to validate its components
    parsed = urllib.parse.urlparse(cdn_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid CDN URL: {cdn_url!r}")

    # Ensure the domain is allowed
    domain = parsed.netloc.lower()
    if domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {domain!r}")

    # Normalise path components to avoid double slashes
    base_path = parsed.path.rstrip("/")
    resource_path = urllib.parse.quote(resource_key.strip("/"))
    category = res_category.strip("/")

    # Construct the final URL
    full_path = f"{base_path}/{category}/{resource_path}"
    # Rebuild the URL preserving scheme and netloc
    final_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            full_path,
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return final_url