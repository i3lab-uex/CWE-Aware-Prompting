import urllib.parse
from typing import Iterable

# A set of CDN domains that are allowed to serve content.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.example.org",
    "static.cdn.net",
}

def generate_cdn_content_url(
    cdn_origin_url: str,
    content_id: str,
    content_kind: str
) -> str:
    """
    Assemble a fully qualified URL for a resource stored on an external CDN.

    Parameters
    ----------
    cdn_origin_url : str
        The base URL of the CDN.  Must include a scheme (e.g., ``https://``).
    content_id : str
        A unique identifier for the resource (e.g., a hash or UUID).
    content_kind : str
        A short string indicating the type of resource (e.g., ``image``, ``script``).

    Returns
    -------
    str
        A fully qualified URL that points to the requested resource on the CDN.

    Raises
    ------
    ValueError
        If the resolved domain is not in :data:`ALLOWED_CDN_DOMAINS` or if
        the constructed URL is malformed.

    Notes
    -----
    The function performs strict domain validation to mitigate CWE-610
    (Externally Controlled Reference to a Resource in Another Sphere).  It also
    normalises the URL components to avoid subtle injection attacks.
    """
    # Parse the base CDN URL
    parsed_base = urllib.parse.urlparse(cdn_origin_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN origin URL: {cdn_origin_url!r}")

    # Ensure the base domain is allowed
    if parsed_base.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {parsed_base.hostname!r}")

    # Construct the path component in a safe way
    # e.g., /{content_kind}/{content_id}
    path = urllib.parse.urljoin(parsed_base.path + "/", f"{urllib.parse.quote(content_kind)}/{urllib.parse.quote(content_id)}")

    # Rebuild the full URL
    final_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    # Final domain validation (redundant but defensive)
    final_parsed = urllib.parse.urlparse(final_url)
    if final_parsed.hostname not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Resolved URL points to disallowed domain: {final_parsed.hostname!r}")

    return final_url