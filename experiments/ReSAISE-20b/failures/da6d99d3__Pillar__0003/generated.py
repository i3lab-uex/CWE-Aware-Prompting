import urllib.parse

# Set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.cdn.net",
}

def build_external_resource_link(cdn_url: str, resource_key: str, res_category: str) -> str:
    """
    Construct a full URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN (e.g. "https://cdn.example.com").
    resource_key : str
        Identifier for the specific resource (e.g. "logo.png").
    res_category : str
        Category of the resource (e.g. "image", "script").

    Returns
    -------
    str
        The fully constructed URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the target domain is not in ``ALLOWED_CDN_DOMAINS`` or if any
        component of the URL is malformed.
    """
    # Parse the CDN base URL and validate its domain
    parsed_cdn = urllib.parse.urlparse(cdn_url)
    if not parsed_cdn.scheme or not parsed_cdn.netloc:
        raise ValueError(f"Invalid CDN URL: {cdn_url!r}")

    # Normalize the domain to lower case for comparison
    cdn_domain = parsed_cdn.netloc.lower()
    if cdn_domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain {cdn_domain!r} is not an allowed CDN")

    # Ensure the resource key and category are safe (no leading slashes or traversal)
    if any(part in {"/", ".."} for part in [resource_key, res_category]):
        raise ValueError("Resource key or category contains disallowed characters")

    # Build the path: /{res_category}/{resource_key}
    resource_path = urllib.parse.urljoin("/", f"{res_category.rstrip('/')}/")
    resource_path = urllib.parse.urljoin(resource_path, resource_key.lstrip("/"))

    # Reconstruct the full URL
    full_url = urllib.parse.urlunparse((
        parsed_cdn.scheme,
        parsed_cdn.netloc,
        resource_path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return full_url