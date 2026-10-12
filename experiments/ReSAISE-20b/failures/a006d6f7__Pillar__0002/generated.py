import urllib.parse
import posixpath

# Set of domains that are allowed to serve CDN content.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.somesite.org",
}

def generate_cdn_content_url(cdn_origin_url: str, content_id: str, content_kind: str) -> str:
    """
    Assemble a fully‑qualified URL for CDN resources.

    Parameters
    ----------
    cdn_origin_url : str
        Base URL of the CDN (e.g. "https://cdn.example.com").
    content_id : str
        Unique identifier for the requested resource.
    content_kind : str
        Resource type (e.g. "image", "script").

    Returns
    -------
    str
        Validated, fully‑qualified URL for the CDN resource.

    Raises
    ------
    ValueError
        If the constructed URL resolves to an unauthorized CDN domain.
    """
    # Parse the base CDN URL
    parsed_origin = urllib.parse.urlparse(cdn_origin_url)
    if not parsed_origin.scheme or not parsed_origin.netloc:
        raise ValueError("cdn_origin_url must be a valid absolute URL")

    # Normalize the path to prevent traversal
    # The content_kind and content_id should not contain slashes or dots.
    for part in (content_kind, content_id):
        if "/" in part or ".." in part:
            raise ValueError("content_kind and content_id must not contain slashes or '..'")

    # Build the new path
    new_path = posixpath.join(parsed_origin.path, content_kind, content_id)

    # Reconstruct the full URL
    url = urllib.parse.urlunparse((
        parsed_origin.scheme,
        parsed_origin.netloc,
        new_path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    # Validate the target domain
    if parsed_origin.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{parsed_origin.netloc}' is not an allowed CDN host")

    return url