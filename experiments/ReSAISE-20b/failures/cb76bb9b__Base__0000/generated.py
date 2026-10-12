import re
from urllib.parse import urljoin, urlparse

# Example set of allowed CDN domains. In real applications this should be
# configured via environment variables or a secure config store.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.securecdn.org",
    "images.mysite.net",
}

# Allowed resource types (you can extend this list as needed).
_ALLOWED_RES_TYPES = {"image", "script", "style", "font"}

# Regular expression to validate resource identifiers (alphanumeric, dashes, underscores).
_RES_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_\-]+$")

def create_resource_url(base_cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Build a fully-qualified CDN URL for a given resource.

    Parameters
    ----------
    base_cdn_url : str
        Base URL of the CDN (e.g. "https://cdn.example.com/").
    res_id : str
        Unique identifier of the resource (e.g. "logo.png").
    res_type : str
        Type of the resource, e.g. "image" or "script".

    Returns
    -------
    str
        The fully-qualified URL to the resource.

    Raises
    ------
    ValueError
        If any argument is invalid or if the resulting URL points to a domain
        that is not in :data:`ALLOWED_CDN_DOMAINS`.
    """
    # ---- Validate the resource type -------------------------------------------------
    if res_type not in _ALLOWED_RES_TYPES:
        raise ValueError(f"Unsupported resource type: {res_type!r}")

    # ---- Validate the resource identifier ------------------------------------------
    if not _RES_ID_PATTERN.match(res_id):
        raise ValueError(f"Invalid resource identifier: {res_id!r}")

    # ---- Normalize and build the URL ------------------------------------------------
    # Ensure base_cdn_url ends with a slash so that urljoin behaves correctly.
    if not base_cdn_url.endswith("/"):
        base_cdn_url += "/"

    # Construct a relative path: "<res_type>/<res_id>"
    relative_path = f"{res_type}/{res_id}"
    full_url = urljoin(base_cdn_url, relative_path)

    # ---- Parse the resulting URL and verify the domain ----------------------------
    parsed = urlparse(full_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL constructed: {full_url!r}")

    # The netloc may include port numbers; strip them for comparison.
    domain = parsed.hostname
    if domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"URL points to disallowed CDN domain: {domain!r}")

    return full_url