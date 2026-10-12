import urllib.parse
import posixpath

# Example set of allowed CDN domains.  In a real application this would be
# defined elsewhere and imported.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.provider.net"
}


def create_resource_url(base_cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Construct a fully qualified URL for a resource hosted on an approved CDN.

    Parameters
    ----------
    base_cdn_url : str
        Base URL of the CDN, e.g. "https://cdn.example.com/".
    res_id : str
        Unique identifier of the resource (typically a file name or hash).
    res_type : str
        Resource type, e.g. "image", "script".  This value is appended as a
        directory in the URL path.

    Returns
    -------
    str
        The fully qualified resource URL.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in
        ``ALLOWED_CDN_DOMAINS``.
    """
    # Normalise the base URL to ensure it ends with a slash
    parsed_base = urllib.parse.urlparse(base_cdn_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base CDN URL: {base_cdn_url!r}")

    # Build the relative path safely using posixpath
    rel_path = posixpath.join(res_type.strip('/'), res_id.strip('/'))
    # Use urljoin to combine base and relative path
    full_url = urllib.parse.urljoin(parsed_base.geturl(), rel_path)

    # Resolve the final URL to ensure no redirects or relative parts
    parsed_full = urllib.parse.urlparse(full_url)

    # Validate the domain against allowed CDN domains
    if parsed_full.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Domain '{parsed_full.netloc}' is not an allowed CDN domain."
        )

    return full_url