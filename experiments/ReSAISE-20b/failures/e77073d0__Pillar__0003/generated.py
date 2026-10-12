import re
from urllib.parse import urlparse, urljoin

# Allowed CDN domains (example list)
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.othercdn.org"
}

def _is_allowed_domain(domain: str) -> bool:
    """
    Check if the given domain is in the allowed CDN list.
    Normalise by lower‑casing and stripping port numbers.
    """
    # Remove any port number
    domain = domain.split(":")[0].lower()
    return domain in ALLOWED_CDN_DOMAINS

def _sanitize_file_id(file_id: str) -> str:
    """
    Reject file IDs that contain suspicious characters or path traversal.
    Only allow alphanumerics, hyphens, underscores and periods.
    """
    if not re.match(r"^[a-zA-Z0-9._\-]+$", file_id):
        raise ValueError("Invalid file_id: contains disallowed characters")
    return file_id

def build_cdn_resource_url(cdn_url_base: str, file_id: str, file_type: str) -> str:
    """
    Assemble a fully qualified CDN URL for the given resource.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN (e.g. "https://cdn.example.com/").
    file_id : str
        Unique identifier for the resource.
    file_type : str
        Resource type (e.g. "image", "script").

    Returns
    -------
    str
        The fully qualified, validated URL.

    Raises
    ------
    ValueError
        If the constructed URL resolves to an unauthorized CDN domain,
        or if inputs contain disallowed characters.
    """
    # Basic sanity checks
    if not isinstance(cdn_url_base, str) or not cdn_url_base:
        raise ValueError("cdn_url_base must be a non-empty string")
    if not isinstance(file_id, str) or not file_id:
        raise ValueError("file_id must be a non-empty string")
    if not isinstance(file_type, str) or not file_type:
        raise ValueError("file_type must be a non-empty string")

    # Sanitize the file_id
    safe_file_id = _sanitize_file_id(file_id)

    # Build candidate URL
    # Ensure base ends with a slash so urljoin works correctly
    if not cdn_url_base.endswith("/"):
        cdn_url_base += "/"
    path = f"{file_type}/{safe_file_id}"
    candidate_url = urljoin(cdn_url_base, path)

    # Validate the domain
    parsed = urlparse(candidate_url)
    if not _is_allowed_domain(parsed.netloc):
        raise ValueError(f"Unauthorized CDN domain: {parsed.netloc}")

    return candidate_url