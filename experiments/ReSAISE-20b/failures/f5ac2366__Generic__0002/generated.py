import urllib.parse
from typing import Set

# Define the set of allowed CDN domains (example values)
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.content.org",
}

def construct_external_resource_url(
    cdn_base_url: str,
    resource_id: str,
    resource_type: str
) -> str:
    """
    Construct a fully qualified URL to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base_url : str
        Base URL of the CDN, e.g. "https://cdn.example.com/"
    resource_id : str
        Identifier of the resource (e.g. "logo.png", "app.min.js")
    resource_type : str
        Type of the resource (e.g. 'image', 'script'). Used only for validation.

    Returns
    -------
    str
        The fully resolved URL to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL does not point to an allowed CDN domain, or if
        parameters are malformed.
    """
    # Basic sanity checks
    if not cdn_base_url or not resource_id or not resource_type:
        raise ValueError("All arguments must be non-empty strings")

    # Normalize base URL: ensure it ends with a slash
    if not cdn_base_url.endswith("/"):
        base = f"{cdn_base_url}/"
    else:
        base = cdn_base_url

    # Prevent directory traversal by rejecting resource_id that starts with '..' or contains
    # absolute paths. This ensures the resource ID is a relative path component.
    if ".." in resource_id.split("/") or urllib.parse.urlparse(resource_id).scheme:
        raise ValueError("resource_id contains unsafe path components")

    # Join base URL with resource ID
    full_url = urllib.parse.urljoin(base, urllib.parse.quote(resource_id))

    # Parse the resulting URL to inspect its components
    parsed = urllib.parse.urlparse(full_url)

    # Validate scheme: only http or https allowed
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate host domain against allowed CDN domains
    if parsed.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{parsed.hostname}' is not in the list of allowed CDN domains")

    # Optionally, validate that resource_type matches expected file extension
    type_to_ext = {
        "image": {".png", ".jpg", ".jpeg", ".gif", ".webp"},
        "script": {".js"},
        "style": {".css"},
    }
    ext = urllib.parse.splitext(parsed.path)[1].lower()
    allowed_exts = type_to_ext.get(resource_type.lower())
    if allowed_exts and ext not in allowed_exts:
        raise ValueError(f"Resource type '{resource_type}' does not match file extension '{ext}'")

    return full_url