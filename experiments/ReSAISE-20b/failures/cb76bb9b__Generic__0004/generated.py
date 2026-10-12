import urllib.parse
from typing import Set

# Example set of allowed CDN domains – replace with the actual list used in your project
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.anothercdn.org",
    "static.myapp.net",
}

def create_resource_url(base_cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Build a secure CDN URL for the requested resource.

    Parameters
    ----------
    base_cdn_url : str
        The base URL of the CDN (e.g. "https://cdn.example.com/").
    res_id : str
        The unique identifier of the resource.
    res_type : str
        Type of the resource (e.g. "image", "script").

    Returns
    -------
    str
        A fully-qualified URL pointing to the resource.

    Raises
    ------
    ValueError
        If the resolved host is not in ``ALLOWED_CDN_DOMAINS``.
    """
    # Normalise the base URL to ensure it ends with a slash
    if not base_cdn_url.endswith("/"):
        base_cdn_url += "/"

    # Construct the relative path
    # Use quote to escape any special characters in res_id and res_type
    rel_path = urllib.parse.quote(f"{res_type}/{res_id}")

    # Join the base URL with the relative path
    full_url = urllib.parse.urljoin(base_cdn_url, rel_path)

    # Parse the URL to extract the hostname
    parsed = urllib.parse.urlparse(full_url)
    host = parsed.hostname

    if not host or host.lower() not in {d.lower() for d in ALLOWED_CDN_DOMAINS}:
        raise ValueError(f"Disallowed CDN domain: {host!r}")

    return full_url