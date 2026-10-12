import urllib.parse
from typing import Set

# Predefined set of domains considered valid for CDNs.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.example.org",
    "static.myapp.net",
}

def create_resource_url(base_cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Build a fully-qualified CDN URL for a given resource.

    Parameters
    ----------
    base_cdn_url : str
        The base URL of the CDN, e.g. "https://cdn.example.com/".
    res_id : str
        Unique identifier of the resource (e.g. a file name or hash).
    res_type : str
        The type of resource, used as part of the path (e.g. "image", "script").

    Returns
    -------
    str
        The fully-qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in ``ALLOWED_CDN_DOMAINS``.
    """
    # Normalise the base URL
    parsed_base = urllib.parse.urlparse(base_cdn_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base CDN URL")

    # Build a relative path: /<res_type>/<res_id>
    # Ensure that res_id is URL-safe by percent-encoding it.
    safe_res_id = urllib.parse.quote(res_id, safe="")
    relative_path = f"/{res_type.strip('/')}/{safe_res_id}"

    # Construct the full URL
    full_url = urllib.parse.urljoin(parsed_base.geturl(), relative_path)

    # Validate the domain
    parsed_full = urllib.parse.urlparse(full_url)
    if parsed_full.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {parsed_full.netloc}")

    return full_url