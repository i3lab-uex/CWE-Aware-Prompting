import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (case‑insensitive)
_TRUSTED_DOMAINS = {
    "example.com",
    "cdn.example.org",
    "images.safe-host.net",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}


def _normalize_domain(domain: str) -> str:
    """
    Normalises a domain name for comparison.
    Removes leading "www." and converts to lower case.
    """
    return domain.lower().lstrip("www.")


def validate_image_source(img_src: str) -> str:
    """
    Validate that the supplied image URL comes from a trusted provider
    and has an allowed scheme. Returns the fully resolved URL.

    Parameters:
        img_src (str): The image URL to validate.

    Returns:
        str: The original, validated URL.

    Raises:
        ValueError: If the URL uses an unsupported scheme or
                    does not belong to a trusted domain.
    """
    if not isinstance(img_src, str):
        raise ValueError("img_src must be a string")

    # Parse the URL
    parsed = urlparse(img_src)

    # Validate scheme
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate domain
    netloc = parsed.netloc
    if not netloc:
        raise ValueError("URL must contain a network location (domain)")

    # Strip port if present
    domain = netloc.split(":")[0]
    normalized_domain = _normalize_domain(domain)

    if not any(normalized_domain == d or normalized_domain.endswith("." + d) for d in _TRUSTED_DOMAINS):
        raise ValueError(f"Untrusted domain: {domain}")

    # Re‑assemble the URL to ensure it is canonical
    cleaned = urlunparse(parsed._replace(netloc=netloc.lower()))
    return cleaned