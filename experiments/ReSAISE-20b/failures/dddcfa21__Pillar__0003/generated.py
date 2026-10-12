import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (case‑insensitive)
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.images.org",
    "pics.safehost.net",
    "secure.imgs.io",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def _normalize_domain(domain: str) -> str:
    """
    Normalize the domain for comparison:
    - Lowercase
    - Strip leading/trailing whitespace
    """
    return domain.strip().lower()


def check_image_url(img_address: str) -> str:
    """
    Validate an image URL and return the resolved full URL if it belongs to
    a trusted domain.

    Parameters
    ----------
    img_address : str
        The input image URL to validate.

    Returns
    -------
    str
        The fully resolved, validated URL.

    Raises
    ------
    ValueError
        If the URL scheme is unsupported, or if the domain is not in the
        trusted list.
    """
    if not isinstance(img_address, str):
        raise ValueError("img_address must be a string")

    parsed = urlparse(img_address)

    # Scheme validation
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Domain normalization and validation
    domain = _normalize_domain(parsed.hostname or "")
    if domain not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {domain}")

    # Reconstruct the URL to ensure it is normalized
    cleaned = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=f"{domain}{':' + str(parsed.port) if parsed.port else ''}",
    )
    return urlunparse(cleaned)