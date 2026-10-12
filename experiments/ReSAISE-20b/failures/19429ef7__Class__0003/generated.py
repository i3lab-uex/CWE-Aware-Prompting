import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (add or remove as needed)
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "upload.wikimedia.org",
    "picsum.photos",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

def fetch_image_url(img_url: str) -> str:
    """
    Validate that the supplied image URL points to a trusted domain and uses an allowed scheme.
    
    Parameters
    ----------
    img_url : str
        The image URL to validate.

    Returns
    -------
    str
        The original URL if it is trusted and valid.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, is malformed, or points to an untrusted domain.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    # Parse the URL
    parsed = urlparse(img_url)

    # Scheme must be http or https
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Domain must be in the trusted list
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid host component")

    # Normalize the hostname (lowercase, strip leading 'www.')
    normalized = hostname.lower()
    if normalized.startswith("www."):
        normalized = normalized[4:]

    if normalized not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {hostname}")

    # Reconstruct the URL to ensure it is canonical
    cleaned = urlunparse(parsed._replace(scheme=parsed.scheme, netloc=hostname))
    return cleaned