import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (add or remove as needed)
_TRUSTED_DOMAINS = {
    "i.imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "flickr.com",
    "imgur.com",
}

# Allowed schemes
_ALLOWED_SCHEMES = {"http", "https"}

def _normalize_domain(domain: str) -> str:
    """
    Normalise the domain for comparison.
    - Lowercase
    - Strip common 'www.' prefix
    """
    domain = domain.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    return domain

def fetch_image_url(img_url: str) -> str:
    """
    Validate an image URL against a whitelist of trusted domains.

    Parameters
    ----------
    img_url : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it passes validation.

    Raises
    ------
    ValueError
        If the scheme is not http/https or the domain is not trusted.
    """
    if not isinstance(img_url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(img_url)

    # Check scheme
    if parsed.scheme not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Resolve relative URLs to absolute by joining with a dummy base
    if not parsed.netloc:
        raise ValueError("URL must contain a network location")

    domain = _normalize_domain(parsed.netloc)

    # Domain whitelist check
    if domain not in _TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {domain}")

    # Reconstruct the URL to ensure it is fully resolved
    normalized = urlunparse(parsed._replace(netloc=parsed.netloc.lower()))
    return normalized