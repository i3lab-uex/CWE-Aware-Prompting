import urllib.parse

# Predefined set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net",
}

def build_external_resource_link(cdn_url: str, resource_key: str, res_category: str) -> str:
    """
    Construct a fully-qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN (e.g., "https://cdn.example.com/").
    resource_key : str
        Identifier for the specific resource (e.g., "12345").
    res_category : str
        Resource category such as 'image', 'script', etc.

    Returns
    -------
    str
        The fully constructed URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL does not target a domain in ALLOWED_CDN_DOMAINS.
    """
    # Parse the CDN base URL to validate its domain
    parsed_cdn = urllib.parse.urlparse(cdn_url)
    if not parsed_cdn.scheme or not parsed_cdn.netloc:
        raise ValueError(f"Invalid CDN URL: {cdn_url}")

    # Normalize the domain (strip 'www.' if present)
    cdn_domain = parsed_cdn.netloc.lower()
    if cdn_domain.startswith("www."):
        cdn_domain = cdn_domain[4:]

    if cdn_domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"CDN domain '{cdn_domain}' is not allowed")

    # Build the path component safely
    # Ensure leading slash for category and resource key, but avoid double slashes
    path = urllib.parse.urljoin("/", f"{res_category.rstrip('/')}/")
    path = urllib.parse.urljoin(path, resource_key.lstrip("/"))

    # Construct the final URL
    final_url = urllib.parse.urlunparse((
        parsed_cdn.scheme,
        parsed_cdn.netloc,
        path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    # Final domain check (in case urljoin altered the netloc)
    final_parsed = urllib.parse.urlparse(final_url)
    final_domain = final_parsed.netloc.lower()
    if final_domain.startswith("www."):
        final_domain = final_domain[4:]

    if final_domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Resulting URL domain '{final_domain}' is not allowed")

    return final_url