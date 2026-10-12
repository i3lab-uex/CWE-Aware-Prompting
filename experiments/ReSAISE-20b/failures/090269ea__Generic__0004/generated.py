import urllib.parse
from typing import Iterable

# Example of allowed CDN domains; in real use this should be defined elsewhere
ALLOWED_CDN_DOMAINS: Iterable[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.content.org",
}


def create_external_resource_link(cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Construct a validated URL pointing to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN, e.g. "https://cdn.example.com".
    res_id : str
        Unique identifier for the resource, e.g. a file hash or path.
    res_type : str
        Type of the resource, e.g. "image" or "script".  This is used as a
        path component to separate resource categories.

    Returns
    -------
    str
        A fully qualified, validated URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resolved CDN domain is not in :data:`ALLOWED_CDN_DOMAINS`.

    Notes
    -----
    The function uses :func:`urllib.parse.urljoin` to safely combine the base
    URL with path components, and performs a strict domain check to prevent
    open redirects or DNS rebinding attacks.
    """
    # Parse the base CDN URL to extract its components
    parsed_base = urllib.parse.urlparse(cdn_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN URL: {cdn_url!r}")

    # Ensure the domain is allowed
    if parsed_base.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Unauthorized CDN domain: {parsed_base.hostname!r}")

    # Normalise resource type and ID to avoid path traversal or double slashes
    safe_res_type = urllib.parse.quote_plus(res_type.strip().lstrip("/"))
    safe_res_id = urllib.parse.quote_plus(res_id.strip().lstrip("/"))

    # Build the relative path
    rel_path = f"/{safe_res_type}/{safe_res_id}"

    # Join with the base URL
    full_url = urllib.parse.urljoin(cdn_url.rstrip("/") + "/", rel_path.lstrip("/"))

    # Final validation: ensure the resulting URL's domain matches the base
    final_parsed = urllib.parse.urlparse(full_url)
    if final_parsed.hostname != parsed_base.hostname:
        raise ValueError("Resulting URL resolves to an unauthorized domain")

    return full_url