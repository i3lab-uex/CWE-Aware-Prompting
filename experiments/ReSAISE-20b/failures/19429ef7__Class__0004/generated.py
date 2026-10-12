import re
from urllib.parse import urlparse, urlunparse

# Define a set of trusted image hosting domains (case‑insensitive)
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "picsum.photos",
    "cdn.example.com",   # add your own trusted domains here
}

# Supported URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def fetch_image_url(img_url: str) -> str:
    """
    Validate that the supplied image URL is from a trusted domain and
    returns the normalized, absolute URL.

    Parameters
    ----------
    img_url : str
        The image URL to validate and resolve.

    Returns
    -------
    str
        The validated, normalized URL.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, is malformed,
        or points to an untrusted domain.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    # Parse the URL
    parsed = urlparse(img_url)

    # Scheme check
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Domain (netloc) must be present
    netloc = parsed.netloc.lower()
    if not netloc:
        raise ValueError("URL must contain a host component")

    # Validate domain against the trusted list
    if not any(netloc == d or netloc.endswith("." + d) for d in TRUSTED_DOMAINS):
        raise ValueError(f"Untrusted domain: {netloc}")

    # Normalize the URL (remove fragment, collapse percent‑encoding)
    normalized = parsed._replace(fragment="", params="")
    # Optionally encode the path and query properly
    normalized = urlunparse(normalized)

    return normalized