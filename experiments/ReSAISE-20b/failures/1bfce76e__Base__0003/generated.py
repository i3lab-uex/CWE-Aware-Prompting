import urllib.parse
from typing import Set

# Predefined set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    # Add other trusted CDN domains here.
}


def generate_external_resource_url(cdn_base: str, res_id: str, res_type: str) -> str:
    """
    Construct a fully-qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base : str
        Base URL of the Content Delivery Network (e.g. "https://cdn.example.com").
    res_id : str
        Identifier of the resource (e.g. a file name or hash).
    res_type : str
        Type/category of the resource (e.g. "image", "script").

    Returns
    -------
    str
        A fully-qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If any argument is not a string, or if the resulting URL resolves to a domain
        that is not in :data:`ALLOWED_CDN_DOMAINS`.
    """
    # Basic type validation
    if not all(isinstance(arg, str) for arg in (cdn_base, res_id, res_type)):
        raise ValueError("All arguments must be strings")

    # Ensure the base URL ends with a slash for correct joining
    if not cdn_base.endswith("/"):
        cdn_base = f"{cdn_base}/"

    # Construct the path component safely
    # Prevent leading slashes or empty components that could cause relative resolution issues.
    safe_res_type = urllib.parse.quote(res_type.strip("/"))
    safe_res_id = urllib.parse.quote(res_id.strip("/"))

    path = f"{safe_res_type}/{safe_res_id}"

    # Resolve the full URL
    full_url = urllib.parse.urljoin(cdn_base, path)

    # Parse the netloc (domain) of the resulting URL
    parsed = urllib.parse.urlparse(full_url)
    domain = parsed.hostname

    if not domain or domain.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {domain}")

    return full_url