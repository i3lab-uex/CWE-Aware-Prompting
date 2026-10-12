import urllib.parse
import posixpath

# Example set of allowed CDN domains.  In real code this would be
# defined elsewhere or imported from a configuration module.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.content.org",
}

def build_cdn_resource_url(cdn_url: str,
                           resource_identifier: str,
                           resource_kind: str) -> str:
    """
    Construct a full CDN URL for a given resource.

    Parameters
    ----------
    cdn_url : str
        Base CDN URL (e.g. "https://cdn.example.com/").
    resource_identifier : str
        Unique identifier for the requested resource. Must be a
        relative path without leading slashes or traversal components.
    resource_kind : str
        The kind of resource (e.g. "image", "script").  It is appended
        as a path component after the identifier.

    Returns
    -------
    str
        A fully qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resolved URL does not belong to an allowed CDN domain,
        or if the resource identifier contains unsafe components.
    """
    # 1. Validate and normalize the resource_identifier
    if not isinstance(resource_identifier, str):
        raise TypeError("resource_identifier must be a string")

    # Remove any leading slashes to keep it relative
    resource_identifier = resource_identifier.lstrip("/")

    # Reject traversal sequences that could escape the intended path
    if ".." in resource_identifier.split("/"):
        raise ValueError("resource_identifier contains unsafe path components")

    # Normalize the path to collapse any redundant separators
    safe_path = posixpath.normpath(resource_identifier)

    # 2. Build the full URL
    # Ensure cdn_url ends with a slash so urljoin appends correctly.
    base = cdn_url if cdn_url.endswith("/") else cdn_url + "/"
    # Append the resource kind and identifier
    full_path = posixpath.join(resource_kind, safe_path)
    full_url = urllib.parse.urljoin(base, full_path)

    # 3. Validate the domain
    parsed = urllib.parse.urlparse(full_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL produced")

    # Extract hostname (ignoring port if present)
    host = parsed.hostname
    if host not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"URL domain '{host}' is not an allowed CDN")

    return full_url