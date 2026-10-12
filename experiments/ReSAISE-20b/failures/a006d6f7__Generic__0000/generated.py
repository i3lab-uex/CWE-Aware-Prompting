import urllib.parse
from typing import Set

# A set of CDN domains that are allowed to be used.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.content.cdn.io",
}

def generate_cdn_content_url(
    cdn_origin_url: str,
    content_id: str,
    content_kind: str
) -> str:
    """
    Construct a fully qualified CDN URL for a given content ID and kind.

    Parameters
    ----------
    cdn_origin_url : str
        Base URL of the CDN. Must include scheme (http/https) and may optionally
        end with a slash.
    content_id : str
        Unique identifier for the requested resource (e.g. image hash).
    content_kind : str
        Type of the content, e.g. "image", "script", "video".

    Returns
    -------
    str
        A validated URL that points to the resource on an allowed CDN.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain that is not in
        ``ALLOWED_CDN_DOMAINS``.
    """
    # Parse the base CDN URL to ensure it contains a scheme and netloc
    parsed_base = urllib.parse.urlparse(cdn_origin_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_origin_url!r}")

    # Normalise the path to avoid double slashes
    base_path = parsed_base.path.rstrip("/")
    # Build the relative path for the content
    rel_path = f"/{content_kind.strip('/')}/{content_id.lstrip('/')}"
    # Join base and relative paths
    full_path = urllib.parse.urljoin(base_path + "/", rel_path.lstrip("/"))

    # Construct the final URL
    full_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",  # params
            "",  # query
            ""   # fragment
        )
    )

    # Validate the domain against the allowed list
    if parsed_base.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"CDN domain '{parsed_base.netloc}' is not authorized."
        )

    return full_url