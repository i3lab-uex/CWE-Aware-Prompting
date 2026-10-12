import re
from urllib.parse import urlparse, urlunparse

# List of approved image hosting domains.
TRUSTED_DOMAINS = {
    "images.unsplash.com",
    "cdn.pixabay.com",
    "i.imgur.com",
    "storage.googleapis.com",
    "images.weserv.nl",
}

# Allowed URL schemes.
ALLOWED_SCHEMES = {"http", "https"}


def fetch_image_url(img_url: str) -> str:
    """
    Validate and return a fully resolved image URL.

    Parameters
    ----------
    img_url : str
        The raw image URL to validate.

    Returns
    -------
    str
        The validated, fully resolved URL.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme or points to an untrusted domain.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    parsed = urlparse(img_url)

    # Scheme check
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Domain check (allow subdomains)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Normalize the domain for comparison
    host = host.lower()
    if not any(host == domain or host.endswith("." + domain) for domain in TRUSTED_DOMAINS):
        raise ValueError(f"Untrusted domain: {host}")

    # Reconstruct the URL to ensure it is fully resolved
    # (e.g., percent-encoding, default ports)
    normalized = urlunparse(parsed._replace())
    return normalized