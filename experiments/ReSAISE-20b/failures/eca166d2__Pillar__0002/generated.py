import re
from urllib.parse import urlparse, urlunparse

# Whitelisted domains (add or remove as needed)
_TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trustedsite.org",
    "pics.safehost.net",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}


def validate_image_source(img_src: str) -> str:
    """
    Validate that the provided image URL belongs to a trusted domain and uses
    an allowed scheme.  The function returns the normalized, fully-qualified URL.

    Parameters
    ----------
    img_src : str
        The image URL to validate and resolve.

    Returns
    -------
    str
        The validated, fully-qualified URL.

    Raises
    ------
    ValueError
        If the URL has an unsupported scheme or belongs to an untrusted domain.
    """
    if not isinstance(img_src, str):
        raise ValueError("Image source must be a string")

    # Parse the URL
    parsed = urlparse(img_src)

    # Ensure scheme is present and allowed
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Extract host and validate against whitelist
    hostname = parsed.hostname or ""
    if not _is_trusted_domain(hostname):
        raise ValueError(f"Untrusted domain: {hostname}")

    # Reconstruct the URL to ensure it is fully-qualified
    normalized = urlunparse(parsed)
    return normalized


def _is_trusted_domain(hostname: str) -> bool:
    """
    Check whether the hostname is exactly or a subdomain of a trusted domain.

    Parameters
    ----------
    hostname : str
        The hostname extracted from the URL.

    Returns
    -------
    bool
        True if the domain is trusted, False otherwise.
    """
    hostname = hostname.lower()
    # Exact match
    if hostname in _TRUSTED_DOMAINS:
        return True

    # Subdomain check: e.g., sub.images.example.com
    for domain in _TRUSTED_DOMAINS:
        if hostname.endswith("." + domain):
            return True

    return False