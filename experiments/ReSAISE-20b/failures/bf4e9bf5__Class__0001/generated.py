import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains.  Add more as needed.
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.example.com",
    "cdn.flickr.com",
}

# Regular expression to validate a URL (basic form).  It is intentionally simple
# because the function only needs to confirm that a scheme and netloc are present.
_URL_REGEX = re.compile(
    r'^(?P<scheme>https?)://(?P<netloc>[^/]+)(?P<path>/.*)?$',
    re.IGNORECASE
)

def resolve_image_url(image_url: str) -> str:
    """
    Validate that *image_url* belongs to a trusted image hosting domain
    and return the canonical URL.

    Parameters
    ----------
    image_url : str
        The image URL to be validated and resolved.

    Returns
    -------
    str
        The canonical form of the URL if it belongs to a trusted domain.

    Raises
    ------
    ValueError
        If the URL does not have a valid scheme, or if its domain is not in
        ``TRUSTED_DOMAINS``.
    """
    # Basic validation of scheme and netloc
    match = _URL_REGEX.match(image_url.strip())
    if not match:
        raise ValueError(f"Malformed URL: {image_url!r}")

    scheme = match.group('scheme').lower()
    netloc = match.group('netloc').lower()
    path   = match.group('path') or ""

    # Normalize the domain: remove port numbers and trailing dots
    netloc = re.sub(r':\d+$', '', netloc).rstrip('.')

    # Check if the domain is trusted.  We allow subdomains of a trusted
    # domain (e.g., `sub.i.imgur.com`) by checking the suffix.
    if not any(netloc == d or netloc.endswith("." + d) for d in TRUSTED_DOMAINS):
        raise ValueError(f"Untrusted domain: {netloc!r}")

    # Reconstruct the URL to ensure consistent formatting.
    resolved = urlunparse((scheme, netloc, path, "", "", ""))
    return resolved