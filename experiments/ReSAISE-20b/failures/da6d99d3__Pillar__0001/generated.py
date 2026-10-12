import urllib.parse
import posixpath

# Predefined set of allowed CDN domains (example)
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net"
}

def build_external_resource_link(cdn_url: str, resource_key: str, res_category: str) -> str:
    """
    Construct a fully-qualified URL to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the Content Delivery Network (e.g., "https://cdn.example.com/").
    resource_key : str
        Identifier for the specific resource (e.g., "logo.png").
    res_category : str
        Resource type/category (e.g., "image", "script").

    Returns
    -------
    str
        The fully constructed URL.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to an allowed CDN domain.
    """

    # Normalize the base CDN URL
    parsed_cdn = urllib.parse.urlparse(cdn_url)
    if not parsed_cdn.scheme or not parsed_cdn.netloc:
        raise ValueError(f"Invalid CDN URL: {cdn_url}")

    # Ensure the scheme is HTTP or HTTPS
    if parsed_cdn.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme '{parsed_cdn.scheme}'. Only http and https are allowed.")

    # Normalise path components to prevent traversal attacks
    base_path = posixpath.normpath(parsed_cdn.path)
    if not base_path.endswith("/"):
        base_path += "/"

    # Build the relative path: {category}/{resource_key}
    rel_path = posixpath.join(res_category.strip("/"), resource_key.lstrip("/"))

    # Join the base path with the relative path
    full_path = posixpath.join(base_path, rel_path)

    # Reconstruct the final URL
    constructed_url = urllib.parse.urlunparse((
        parsed_cdn.scheme,
        parsed_cdn.netloc,
        full_path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    # Validate the target domain against the allowed list
    if parsed_cdn.netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{parsed_cdn.netloc}' is not an allowed CDN domain.")

    return constructed_url