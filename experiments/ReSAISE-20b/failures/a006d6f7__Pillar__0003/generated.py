import urllib.parse
from typing import Iterable

# A set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.content.org",
}

def generate_cdn_content_url(
    cdn_origin_url: str,
    content_id: str,
    content_kind: str
) -> str:
    """
    Assemble a fully‑qualified CDN URL for the requested content.

    Parameters
    ----------
    cdn_origin_url : str
        Base URL of the CDN (e.g. "https://cdn.example.com/").
    content_id : str
        Unique identifier of the resource.
    content_kind : str
        Type/category of the content (e.g. "image", "script").

    Returns
    -------
    str
        The validated, absolute URL pointing to the content.

    Raises
    ------
    ValueError
        If the resolved domain is not in ``ALLOWED_CDN_DOMAINS`` or if
        the URL is malformed.
    """
    # Parse the base CDN URL and validate its components
    parsed_origin = urllib.parse.urlparse(cdn_origin_url)
    if not parsed_origin.scheme or parsed_origin.scheme.lower() not in ("http", "https"):
        raise ValueError("CDN URL must use http or https scheme.")

    # Normalise netloc (remove port for comparison)
    origin_netloc = parsed_origin.netloc.split(":")[0].lower()
    if origin_netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Unauthorized CDN domain: {origin_netloc}")

    # Build the path ensuring no relative traversal is possible
    safe_kind = urllib.parse.quote(content_kind.strip("/"), safe="")
    safe_id = urllib.parse.quote(content_id.strip("/"), safe="")

    # Construct the full path
    base_path = parsed_origin.path.rstrip("/")
    full_path = f"{base_path}/{safe_kind}/{safe_id}"

    # Re‑assemble the URL
    final_url = urllib.parse.urlunparse((
        parsed_origin.scheme,
        parsed_origin.netloc,
        full_path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return final_url