import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (case‑insensitive)
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trustedsite.org",
    "pics.safehost.net",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def _normalize_domain(domain: str) -> str:
    """
    Normalizes a domain by stripping leading/trailing whitespace and converting to lowercase.
    """
    return domain.strip().lower()


def check_image_url(img_address: str) -> str:
    """
    Validate an image URL against a list of trusted domains.

    Parameters
    ----------
    img_address : str
        The input image URL to validate.

    Returns
    -------
    str
        The validated, fully resolved URL (identical to the input if it passes checks).

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP/HTTPS or if the host is not in the trusted list.
    """
    if not isinstance(img_address, str):
        raise ValueError("img_address must be a string")

    # Parse the URL
    parsed = urlparse(img_address)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure netloc (host) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a host component")

    # Extract hostname (without port)
    host = parsed.hostname
    if not host:
        raise ValueError("Unable to determine hostname from URL")

    # Normalize and check against trusted domains
    normalized_host = _normalize_domain(host)
    if normalized_host not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted host: {host}")

    # Reconstruct the URL to ensure consistency (e.g., default ports removed)
    cleaned = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=f"{normalized_host}:{parsed.port}" if parsed.port else normalized_host,
    )
    return urlunparse(cleaned)