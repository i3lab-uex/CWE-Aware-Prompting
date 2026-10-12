import re
from urllib.parse import urlparse, urlunparse

# List of approved image hosting domains (case‑insensitive)
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "picsum.photos",
    "flickr.com",
    "images.unsplash.com",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def _is_trusted_domain(domain: str) -> bool:
    """
    Check if a domain is in the trusted list, supporting subdomains
    that are explicitly listed.
    """
    # Normalize to lower case for comparison
    domain = domain.lower()
    return any(domain == d or domain.endswith("." + d) for d in TRUSTED_DOMAINS)


def fetch_image_url(img_url: str) -> str:
    """
    Validate an image URL against a whitelist of trusted domains.

    Parameters
    ----------
    img_url : str
        The URL to validate and resolve.

    Returns
    -------
    str
        The fully resolved, validated URL.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, or its domain is not trusted.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    # Parse the URL
    parsed = urlparse(img_url)

    # Validate scheme
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate domain
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")
    if not _is_trusted_domain(parsed.hostname):
        raise ValueError(f"Untrusted domain: {parsed.hostname}")

    # Reconstruct the URL to ensure a consistent format
    normalized = urlunparse(
        (
            parsed.scheme.lower(),
            parsed.netloc,
            parsed.path or "",
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return normalized