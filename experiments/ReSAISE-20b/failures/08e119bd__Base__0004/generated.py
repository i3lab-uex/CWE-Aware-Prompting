import urllib.parse
from pathlib import Path

# Predefined set of allowed CDN domains.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net",
}

def generate_external_resource_link(
    cdn_host_url: str,
    resource_tag: str,
    resource_category: str
) -> str:
    """
    Build a secure URL pointing to a resource on an external CDN.

    Parameters
    ----------
    cdn_host_url : str
        Base URL of the CDN, e.g. "https://cdn.example.com".
    resource_tag : str
        Unique identifier for the requested resource, e.g. "logo.svg".
    resource_category : str
        Resource type/category (e.g., "image", "script").

    Returns
    -------
    str
        The fully-qualified URL for the resource.

    Raises
    ------
    ValueError
        If the constructed URL does not resolve to an allowed CDN domain.
    """
    # Parse the base CDN URL
    parsed_cdn = urllib.parse.urlparse(cdn_host_url)

    # Validate scheme (must be http or https)
    if parsed_cdn.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed_cdn.scheme}'. Only http/https are allowed.")

    # Ensure the host is in the allowed list
    if parsed_cdn.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain '{parsed_cdn.hostname}' is not an allowed CDN.")

    # Construct the resource path safely
    # Normalise to avoid '..' or other traversal attempts
    safe_tag = urllib.parse.quote_plus(resource_tag)
    # Ensure category does not contain slashes or dangerous chars
    safe_category = urllib.parse.quote_plus(resource_category)

    # Build the path using pathlib for POSIX semantics
    resource_path = Path(safe_category) / safe_tag

    # Join the base URL with the new path
    full_url = urllib.parse.urljoin(
        parsed_cdn.geturl(),
        resource_path.as_posix()
    )

    # Final check: the resulting host must still be allowed
    final_parsed = urllib.parse.urlparse(full_url)
    if final_parsed.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError("Resulting URL points to an unapproved domain.")

    return full_url