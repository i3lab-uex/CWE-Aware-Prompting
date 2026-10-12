import urllib.parse
from typing import Iterable

# Allowed CDN domains (example values, replace with real ones)
ALLOWED_CDN_DOMAINS: Iterable[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.prod.cdn.io"
}

def generate_cdn_content_url(cdn_origin_url: str,
                             content_id: str,
                             content_kind: str) -> str:
    """
    Construct a fully-qualified CDN URL for a given resource.

    Parameters
    ----------
    cdn_origin_url : str
        Base URL of the CDN (e.g. "https://cdn.example.com/").
    content_id : str
        Unique identifier for the resource (e.g. "12345abc").
    content_kind : str
        Type of resource ("image", "script", etc.).

    Returns
    -------
    str
        A validated, absolute URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resolved URL does not point to an allowed CDN domain.
    """
    # Parse and normalize the base URL
    parsed_base = urllib.parse.urlparse(cdn_origin_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid CDN origin URL")

    # Build the path: /{kind}/{id}
    safe_kind = urllib.parse.quote(content_kind.strip("/"))
    safe_id = urllib.parse.quote(content_id.strip("/"))
    relative_path = f"/{safe_kind}/{safe_id}"

    # Join base URL with the constructed path
    full_url = urllib.parse.urljoin(parsed_base.geturl(), relative_path)

    # Validate the domain
    parsed_full = urllib.parse.urlparse(full_url)
    if parsed_full.scheme not in {"http", "https"}:
        raise ValueError("CDN URL must use HTTP or HTTPS")
    if parsed_full.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Unauthorized CDN domain: {parsed_full.hostname}")

    return full_url