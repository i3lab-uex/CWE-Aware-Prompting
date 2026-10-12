import urllib.parse
from typing import Set

# Allowed CDN domains (example set – replace with real values in production)
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.cdn.net",
}

def construct_external_resource_url(
    cdn_base_url: str,
    resource_id: str,
    resource_type: str,
) -> str:
    """
    Construct a fully‑qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base_url : str
        Base URL of the CDN, e.g. "https://cdn.example.com".
    resource_id : str
        Identifier of the requested resource (e.g. image filename).
    resource_type : str
        Type of resource, e.g. "image", "script".

    Returns
    -------
    str
        A complete URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to a domain in ``ALLOWED_CDN_DOMAINS``.
    """
    # Sanitize inputs: strip leading/trailing whitespace and slashes
    cdn_base_url = cdn_base_url.strip()
    resource_id = resource_id.lstrip("/").rstrip("/")
    resource_type = resource_type.strip().lower()

    # Build the relative path
    relative_path = f"{resource_type}/{resource_id}"

    # Resolve against the base URL
    full_url = urllib.parse.urljoin(cdn_base_url.rstrip("/") + "/", relative_path)

    # Parse the resulting URL to inspect its components
    parsed = urllib.parse.urlparse(full_url)

    # Ensure the scheme is HTTP(S)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate that the hostname is in the allowed list
    host = parsed.hostname
    if not host or host.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {host}")

    # Return the fully qualified URL
    return full_url