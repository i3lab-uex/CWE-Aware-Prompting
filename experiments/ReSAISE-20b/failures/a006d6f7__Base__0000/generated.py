import urllib.parse
from typing import Iterable

# Set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS: set[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.content.org",
}


def generate_cdn_content_url(
    cdn_origin_url: str,
    content_id: str,
    content_kind: str,
) -> str:
    """
    Construct a full, validated URL for a CDN resource.

    Parameters
    ----------
    cdn_origin_url : str
        Base URL of the CDN. Must include scheme (http/https).
    content_id : str
        Unique identifier for the resource.
    content_kind : str
        Type of the resource (e.g., 'image', 'script').

    Returns
    -------
    str
        Fully qualified, validated URL pointing to the resource on the CDN.

    Raises
    ------
    ValueError
        If the constructed URL points to a domain not in ``ALLOWED_CDN_DOMAINS``.
    """
    # Parse the base CDN URL
    parsed_base = urllib.parse.urlparse(cdn_origin_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid CDN origin URL")

    # Ensure the base domain is allowed
    if parsed_base.netloc.lower() not in (d.lower() for d in ALLOWED_CDN_DOMAINS):
        raise ValueError(f"Unauthorized CDN domain: {parsed_base.netloc}")

    # Build the relative path to the resource
    # We encode the content_id and kind to prevent path traversal or injection.
    safe_content_id = urllib.parse.quote(content_id, safe="")
    safe_kind = urllib.parse.quote(content_kind, safe="")

    relative_path = f"/{safe_kind}/{safe_content_id}"

    # Join the base URL with the relative path
    full_url = urllib.parse.urljoin(cdn_origin_url.rstrip("/") + "/", relative_path.lstrip("/"))

    # Final safety check: ensure the resulting domain is still allowed
    final_parsed = urllib.parse.urlparse(full_url)
    if final_parsed.netloc.lower() not in (d.lower() for d in ALLOWED_CDN_DOMAINS):
        raise ValueError(f"Redirected to unauthorized domain: {final_parsed.netloc}")

    return full_url