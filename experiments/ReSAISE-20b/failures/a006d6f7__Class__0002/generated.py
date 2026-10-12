import urllib.parse
from typing import Iterable

# Example set of allowed CDN domains. Replace with your actual list.
ALLOWED_CDN_DOMAINS: Iterable[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.somesite.org",
}

def generate_cdn_content_url(
    cdn_origin_url: str,
    content_id: str,
    content_kind: str
) -> str:
    """
    Build a fully-qualified URL for a resource on an approved CDN.

    Parameters
    ----------
    cdn_origin_url : str
        The base URL of the CDN (e.g. "https://cdn.example.com").
    content_id : str
        Unique identifier of the resource (e.g. "abc123").
    content_kind : str
        Type/category of the resource (e.g. "image", "script").

    Returns
    -------
    str
        A fully-qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resolved CDN domain is not in ``ALLOWED_CDN_DOMAINS``.
    """
    # Parse the origin URL to extract its components
    parsed_origin = urllib.parse.urlparse(cdn_origin_url)
    if not parsed_origin.scheme or not parsed_origin.netloc:
        raise ValueError(f"Invalid CDN origin URL: {cdn_origin_url!r}")

    # Ensure the domain is approved
    if parsed_origin.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Unapproved CDN domain: {parsed_origin.hostname!r}. "
            f"Allowed domains are: {', '.join(sorted(ALLOWED_CDN_DOMAINS))}"
        )

    # Construct the path component safely
    # Remove any leading slashes to avoid overriding the origin path.
    clean_kind = content_kind.strip("/").lstrip("./")
    clean_id = content_id.strip("/").lstrip("./")

    # Build the relative path: e.g., "image/abc123"
    rel_path = urllib.parse.quote(f"{clean_kind}/{clean_id}")

    # Combine the origin with the relative path
    full_url = urllib.parse.urljoin(parsed_origin.geturl() + "/", rel_path)

    return full_url