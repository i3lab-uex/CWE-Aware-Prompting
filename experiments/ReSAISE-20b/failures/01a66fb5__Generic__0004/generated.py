import urllib.parse

# Example allowed CDN domains – replace with real ones in production.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "static.myapp.org",
    "assets.somecdn.net",
}

def create_cdn_resource_link(cdn_url_base: str,
                              resource_identifier: str,
                              type_of_resource: str) -> str:
    """
    Build a full CDN URL for a given resource.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN (e.g. 'https://cdn.example.com')
    resource_identifier : str
        Identifier of the requested resource (e.g. 'logo.png')
    type_of_resource : str
        Resource type, used as a sub‑path (e.g. 'image', 'script')

    Returns
    -------
    str
        The fully qualified CDN URL.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain not in ALLOWED_CDN_DOMAINS.
    """
    # Normalise the base URL – strip trailing slashes and ensure a scheme
    if not cdn_url_base.startswith(("http://", "https://")):
        raise ValueError("cdn_url_base must start with http:// or https://")

    # Build the path: /{type_of_resource}/{resource_identifier}
    # Ensure no leading/trailing slashes cause double slashes
    path = f"/{type_of_resource.strip('/')}/{resource_identifier.lstrip('/')}"
    full_url = urllib.parse.urljoin(cdn_url_base.rstrip("/") + "/", path.lstrip("/"))

    # Validate the domain
    parsed = urllib.parse.urlparse(full_url)
    if parsed.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{parsed.netloc}' is not an allowed CDN domain")

    return full_url