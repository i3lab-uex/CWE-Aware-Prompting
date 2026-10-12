import re
from urllib.parse import urlparse

# Trusted image hosting domains (add more as needed)
_TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "storage.googleapis.com",
    "images.weserv.nl",  # example CDN
}

# Allowed schemes
_ALLOWED_SCHEMES = {"http", "https"}

def _is_trusted_domain(netloc: str) -> bool:
    """
    Check if the given netloc (host part of a URL) ends with one of the trusted domains.
    This allows subdomains like 'sub.i.imgur.com' to be accepted as well.
    """
    # Remove port if present
    host = netloc.split(":")[0].lower()
    return any(host == domain or host.endswith("." + domain) for domain in _TRUSTED_DOMAINS)

def check_image_link(image_link: str) -> str:
    """
    Verify that `image_link` points to a trusted image hosting service.

    Parameters
    ----------
    image_link : str
        The URL of the image to validate.

    Returns
    -------
    str
        The original URL if it is considered safe and trusted.

    Raises
    ------
    ValueError
        If the URL has an unsupported scheme, is malformed,
        or does not belong to a trusted domain.
    """
    if not isinstance(image_link, str):
        raise ValueError("image_link must be a string")

    # Basic URL parsing
    parsed = urlparse(image_link)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {image_link}")

    # Ensure scheme is HTTP(S)
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}' in {image_link}")

    # Ensure the host is trusted
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not trusted for image links")

    # Reconstruct the URL to normalize it (e.g., remove fragments)
    safe_url = parsed._replace(fragment="").geturl()

    return safe_url