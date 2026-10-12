import urllib.parse

# Example set of allowed CDN domains; in a real project this would be defined elsewhere
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.otherdomain.net",
}

def build_external_resource_link(cdn_url: str, resource_key: str, res_category: str) -> str:
    """
    Construct a URL pointing to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the Content Delivery Network (e.g., "https://cdn.example.com").
    resource_key : str
        Identifier for the requested resource (e.g., "logo.png").
    res_category : str
        Resource category such as 'image', 'script', etc.

    Returns
    -------
    str
        The fully constructed URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resolved domain is not in ALLOWED_CDN_DOMAINS.
    """
    # Parse the base CDN URL
    parsed_cdn = urllib.parse.urlparse(cdn_url)

    # Normalise scheme and netloc (domain)
    if not parsed_cdn.scheme:
        raise ValueError(f"cdn_url must include a scheme (http/https), got: {cdn_url}")

    # Validate domain against allowed list
    domain = parsed_cdn.netloc.lower()
    if domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not an allowed CDN domain")

    # Construct the path: /<category>/<resource_key>
    # Ensure no double slashes and proper encoding
    path_parts = [res_category.strip('/'), resource_key.lstrip('/')]
    encoded_path = urllib.parse.quote(urllib.parse.urljoin('/', '/'.join(path_parts)))

    # Rebuild the full URL with original scheme and netloc
    final_url = urllib.parse.urlunparse((
        parsed_cdn.scheme,
        domain,
        encoded_path,
        '',  # params
        '',  # query
        ''   # fragment
    ))

    return final_url