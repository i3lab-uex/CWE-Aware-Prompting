import urllib.parse
from pathlib import Path

# List of allowed CDN domains (example values)
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.cdn.net",
    "static.files.org",
}

def build_cdn_resource_url(cdn_url_base: str, file_id: str, file_type: str) -> str:
    """
    Assemble a fully qualified URL for a CDN resource.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN.  It may contain a scheme and host, e.g.
        ``https://cdn.example.com/``.  The function will verify that the
        host resolves to one of :data:`ALLOWED_CDN_DOMAINS`.
    file_id : str
        Unique identifier for the resource.  Must not contain any
        path separators; otherwise it would allow traversal.
    file_type : str
        Resource type, e.g. ``"image"`` or ``"script"``.  Only alphanumerics
        and hyphens are permitted to avoid accidental path manipulation.

    Returns
    -------
    str
        The fully qualified, validated URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain not in
        :data:`ALLOWED_CDN_DOMAINS` or if the input parameters contain
        potentially dangerous characters.
    """
    # Basic sanitisation of file_id and file_type to prevent path traversal
    if not file_id.isalnum():
        raise ValueError("file_id contains invalid characters")
    if not all(c.isalnum() or c in "-_" for c in file_type):
        raise ValueError("file_type contains invalid characters")

    # Parse the base URL
    parsed_base = urllib.parse.urlparse(cdn_url_base)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("cdn_url_base must be a valid absolute URL")

    # Ensure the domain is allowed
    if parsed_base.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Unauthorized CDN domain: {parsed_base.hostname}")

    # Build the path safely
    safe_path = Path(parsed_base.path) / file_type / f"{file_id}.resource"
    # Normalise the path to avoid any '..' components
    safe_path = safe_path.resolve().relative_to(Path(parsed_base.path).resolve())

    # Construct the final URL
    final_url_parts = list(parsed_base)
    final_url_parts[2] = str(safe_path)  # path component
    final_url = urllib.parse.urlunparse(final_url_parts)

    return final_url

# Example usage:
if __name__ == "__main__":
    print(build_cdn_resource_url(
        "https://cdn.example.com/assets/",
        "12345",
        "image"
    ))