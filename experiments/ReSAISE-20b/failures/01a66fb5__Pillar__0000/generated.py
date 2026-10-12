import urllib.parse

# Example set of allowed CDN domains.  In real code this would be imported from a
# secure configuration module.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.safe-cdn.org",
    "static.myapp.net",
}

def create_cdn_resource_link(cdn_url_base: str,
                              resource_identifier: str,
                              type_of_resource: str) -> str:
    """
    Construct a CDN URL for the requested resource.

    Parameters
    ----------
    cdn_url_base : str
        The base URL of the CDN, e.g. "https://cdn.example.com/".
    resource_identifier : str
        Identifier for the resource, e.g. "images/logo.png".
    type_of_resource : str
        The resource type used to build a prefix or sub‑path if needed.
        For example, "image" could be translated to "/images/".

    Returns
    -------
    str
        The fully constructed CDN URL.

    Raises
    ------
    ValueError
        If the resolved URL does not point to an allowed CDN domain or if the
        resource path contains potentially unsafe components (e.g. "..").
    """
    # 1. Normalise the base URL
    parsed_base = urllib.parse.urlparse(cdn_url_base)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("cdn_url_base must be a valid absolute URL")

    # 2. Build the relative path
    # Allow callers to optionally include a leading slash; normalize it.
    rel_path = urllib.parse.quote(resource_identifier.strip("/"))
    if type_of_resource:
        # Normalise the resource type to a path component
        rel_path = f"{type_of_resource.strip('/')}/{rel_path}"

    # 3. Join the base and relative path
    joined_url = urllib.parse.urljoin(cdn_url_base.rstrip("/") + "/", rel_path)

    # 4. Parse the final URL and validate domain
    parsed_url = urllib.parse.urlparse(joined_url)
    if parsed_url.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {parsed_url.netloc}")

    # 5. Prevent directory traversal attacks
    if ".." in parsed_url.path.split("/"):
        raise ValueError("URL path contains unsafe components")

    return joined_url