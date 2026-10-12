import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (case‑insensitive)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "storage.googleapis.com",
    "picsum.photos",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}


def validate_image_source(img_src: str) -> str:
    """
    Validate that an image URL points to a trusted domain and uses a supported scheme.

    Parameters
    ----------
    img_src : str
        The image URL to validate.

    Returns
    -------
    str
        The fully resolved, normalized URL if it is trusted and valid.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, is not absolute, or does not belong to a trusted domain.
    """
    if not isinstance(img_src, str):
        raise ValueError("Image source must be a string")

    # Parse the URL
    parsed = urlparse(img_src)

    # Ensure scheme and netloc are present (absolute URL)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Image source must be an absolute URL")

    # Scheme validation
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Domain normalization (lowercase, strip port)
    hostname = parsed.hostname.lower() if parsed.hostname else ""
    # Strip leading 'www.' for comparison
    hostname = re.sub(r"^www\.", "", hostname)

    # Check if the host is in the trusted list
    if not any(hostname == domain or hostname.endswith("." + domain) for domain in _TRUSTED_DOMAINS):
        raise ValueError(f"Untrusted image host: {hostname}")

    # Reconstruct the URL to ensure it is normalized
    normalized = urlunparse(parsed._replace(scheme=parsed.scheme.lower(), netloc=hostname))
    return normalized