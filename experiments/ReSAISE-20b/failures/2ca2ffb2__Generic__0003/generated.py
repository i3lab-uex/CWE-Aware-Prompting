import re
from urllib.parse import urlparse

# List of approved image hosting domains (add or remove as needed)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "flickr.com",
    "static.tumblr.com",
    "cdn.pixiv.net",
    "s3.amazonaws.com",  # example of a specific bucket domain
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}


def _is_trusted_domain(netloc: str) -> bool:
    """
    Check whether the given netloc belongs to one of the trusted domains.
    The check is performed in a way that prevents subdomain spoofing.

    Examples:
        - 'i.imgur.com' -> True
        - 'sub.i.imgur.com' -> True
        - 'evil.com.imgur.com' -> False
    """
    # Normalize: strip port if present (e.g., example.com:8080)
    host = netloc.split(":")[0].lower()

    # Exact match
    if host in _TRUSTED_DOMAINS:
        return True

    # Subdomain match: host ends with '.' + domain
    for domain in _TRUSTED_DOMAINS:
        if host.endswith("." + domain):
            return True

    return False


def fetch_image_url(url: str) -> str:
    """
    Resolve and validate an image URL against a whitelist of trusted domains.

    Parameters
    ----------
    url : str
        The original image URL to validate.

    Returns
    -------
    str
        The same URL if it is valid and belongs to a trusted domain.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP/HTTPS or if the domain is not trusted.
    """
    # Basic validation
    if not isinstance(url, str) or not url:
        raise ValueError("URL must be a non-empty string")

    parsed = urlparse(url)

    # Check scheme
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate domain
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not trusted")

    # Reconstruct URL to ensure consistency (e.g., lowercasing scheme)
    cleaned_url = parsed.geturl()
    return cleaned_url