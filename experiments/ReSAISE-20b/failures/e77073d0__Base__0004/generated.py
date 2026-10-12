import urllib.parse
from typing import Iterable

# List or set of approved CDN domains (example values)
ALLOWED_CDN_DOMAINS: Iterable[str] = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net",
}

def build_cdn_resource_url(cdn_url_base: str, file_id: str, file_type: str) -> str:
    """
    Assemble a fully qualified URL to a CDN resource.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN.  It may include a scheme and/or path.
    file_id : str
        Unique identifier for the resource (e.g. a hash or UUID).
    file_type : str
        Resource type, used to construct the relative path.

    Returns
    -------
    str
        Fully qualified URL that points to the requested resource.

    Raises
    ------
    ValueError
        If the resolved URL points to a domain that is not in
        ``ALLOWED_CDN_DOMAINS`` or if the URL is malformed.
    """
    # Normalise base URL
    parsed_base = urllib.parse.urlparse(cdn_url_base)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("cdn_url_base must include a valid scheme and host")

    # Construct the relative path: /{file_type}/{file_id}
    relative_path = urllib.parse.urljoin("/", f"{urllib.parse.quote(file_type)}/{urllib.parse.quote(file_id)}")

    # Build the full URL
    full_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        relative_path,
        '',  # params
        '',  # query
        ''   # fragment
    ))

    # Validate the host against allowed domains
    if parsed_base.netloc.lower() not in (d.lower() for d in ALLOWED_CDN_DOMAINS):
        raise ValueError(f"Unapproved CDN domain: {parsed_base.netloc}")

    return full_url