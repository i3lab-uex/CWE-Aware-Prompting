import urllib.parse
from typing import Iterable, Set

# A set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "static.myapp.org",
    # Add additional approved domains here.
}


def create_external_resource_link(cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Build a fully‑qualified URL to an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_url : str
        The base URL of the CDN. Must include a scheme (http:// or https://).
    res_id : str
        The unique identifier for the resource. Will be URL‑escaped.
    res_type : str
        A string indicating the type of resource (e.g., 'image', 'script').
        Will be URL‑escaped.

    Returns
    -------
    str
        A fully resolved and validated CDN URL.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in
        :data:`ALLOWED_CDN_DOMAINS`.
    """
    # Validate that the base CDN URL has a scheme.
    parsed_cdn = urllib.parse.urlparse(cdn_url)
    if not parsed_cdn.scheme or not parsed_cdn.netloc:
        raise ValueError("cdn_url must be a valid absolute URL with scheme and host")

    # Ensure the CDN domain is allowed.
    if parsed_cdn.netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Unauthorized CDN domain: {parsed_cdn.netloc}")

    # Build a safe path by escaping components.
    escaped_id = urllib.parse.quote(res_id, safe='')
    escaped_type = urllib.parse.quote(res_type, safe='')

    # Construct the relative path; e.g. "/image/12345.png"
    resource_path = urllib.parse.urljoin(f"/{escaped_type}/", escaped_id)

    # Join the base CDN URL with the relative path.
    full_url = urllib.parse.urljoin(cdn_url.rstrip('/') + '/', resource_path.lstrip('/'))

    # Final check: the resolved URL's domain must still be allowed.
    final_parsed = urllib.parse.urlparse(full_url)
    if final_parsed.netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Resulting URL resolves to unauthorized domain: {final_parsed.netloc}")

    return full_url