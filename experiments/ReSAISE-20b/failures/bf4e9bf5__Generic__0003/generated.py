import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (case‑insensitive)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "cdn.pixabay.com",
    "flickr.com",
    "images.unsplash.com",
}

# Regular expression to validate a basic HTTP/HTTPS URL
_URL_RE = re.compile(
    r"^(?P<scheme>https?)://(?P<host>[A-Za-z0-9.-]+)(?::\d+)?(?P<path>/[^\s]*)?$",
    re.IGNORECASE,
)


def resolve_image_url(image_url: str) -> str:
    """
    Resolve an image URL after verifying that its domain is trusted.

    Parameters
    ----------
    image_url : str
        The URL of the image to resolve.

    Returns
    -------
    str
        The canonical, resolved URL if it belongs to a trusted domain.

    Raises
    ------
    ValueError
        If the URL is malformed or its host is not in the trusted list.
    """
    if not isinstance(image_url, str):
        raise ValueError("image_url must be a string")

    match = _URL_RE.match(image_url)
    if not match:
        raise ValueError(f"Malformed URL: {image_url!r}")

    scheme = match.group("scheme").lower()
    host = match.group("host").lower()
    path = match.group("path") or ""

    if host not in _TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {host!r}")

    # Reconstruct the URL to ensure a consistent format
    canonical = urlunparse((scheme, host, path, "", "", ""))
    return canonical