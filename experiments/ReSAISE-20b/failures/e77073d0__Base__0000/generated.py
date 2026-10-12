import urllib.parse
from typing import Iterable

# Example set of allowed CDN domains – replace with your actual list.
ALLOWED_CDN_DOMAINS: Iterable[str] = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.otherdomain.org",
}

def build_cdn_resource_url(cdn_url_base: str, file_id: str, file_type: str) -> str:
    """
    Construct a fully-qualified CDN URL for a resource.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN, e.g. "https://cdn.example.com/"
    file_id : str
        Unique identifier for the resource (e.g. a hash or UUID).
    file_type : str
        Resource type, used as part of the path (e.g. "image", "script").

    Returns
    -------
    str
        The fully-qualified URL pointing to the resource.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain not in :data:`ALLOWED_CDN_DOMAINS`
        or if the input is malformed.
    """
    # Sanitize inputs: reject empty values
    if not all([cdn_url_base, file_id, file_type]):
        raise ValueError("All arguments must be non-empty strings")

    # Ensure the base ends with a slash to avoid accidental path concatenation
    if not cdn_url_base.endswith("/"):
        cdn_url_base += "/"

    # Build the relative path. Use quote to avoid injection of special chars.
    relative_path = urllib.parse.quote_plus(file_type.strip()) + "/" + urllib.parse.quote_plus(file_id.strip())

    # Construct the full URL
    full_url = urllib.parse.urljoin(cdn_url_base, relative_path)

    # Parse the URL to validate the domain
    parsed = urllib.parse.urlparse(full_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Resulting URL is malformed")

    # Normalize the domain (strip port if present)
    netloc = parsed.hostname
    if netloc is None:
        raise ValueError("Unable to determine host from URL")

    # Ensure the domain is explicitly listed
    if netloc.lower() not in (d.lower() for d in ALLOWED_CDN_DOMAINS):
        raise ValueError(f"Domain '{netloc}' is not an allowed CDN")

    # Rebuild the URL to ensure canonical form (e.g., lower-case scheme/host)
    safe_url = urllib.parse.urlunparse((
        parsed.scheme.lower(),
        parsed.netloc.lower(),
        parsed.path,
        parsed.params,
        parsed.query,
        parsed.fragment
    ))

    return safe_url