import re
from urllib.parse import urlparse, urlunparse

# List of approved image hosting domains.
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trusted.com",
    "assets.safe.org",
}

# Allowed URL schemes.
ALLOWED_SCHEMES = {"http", "https"}

def get_image_link(link_image: str) -> str:
    """
    Validate an image URL and return the resolved absolute URL.

    Parameters
    ----------
    link_image : str
        The image URL to validate and resolve.

    Returns
    -------
    str
        The validated, absolute image URL.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, is not absolute,
        or does not belong to a trusted domain.
    """
    if not isinstance(link_image, str):
        raise ValueError("link_image must be a string")

    # Parse the URL.
    parsed = urlparse(link_image)

    # Ensure scheme is allowed.
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure host is present.
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Normalize the domain to lowercase for comparison.
    host = parsed.hostname.lower()

    # Check if hostname ends with a trusted domain.
    if not any(host == td or host.endswith("." + td) for td in TRUSTED_DOMAINS):
        raise ValueError(f"Untrusted domain: {host}")

    # Reconstruct the URL to ensure it is absolute and canonical.
    resolved = urlunparse(parsed)

    return resolved