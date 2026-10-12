import re
from urllib.parse import urlparse, urlunparse

# A whitelist of trusted image hosting domains (case‑insensitive).
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.safeimg.org",
    "media.trustedsite.net",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def _normalize_domain(domain: str) -> str:
    """
    Normalises a domain for comparison.  Removes leading `www.` and
    converts to lowercase.
    """
    return domain.lower().lstrip("www.")


def fetch_image_url(img_url: str) -> str:
    """
    Validate that an image URL is from a trusted provider and return the
    canonical absolute URL.

    Parameters
    ----------
    img_url : str
        The image URL to validate.

    Returns
    -------
    str
        A normalised absolute URL if the domain is trusted and scheme allowed.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, is not absolute,
        or points to an untrusted domain.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    # Parse the URL
    parsed = urlparse(img_url)

    # Scheme must be http or https
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP/HTTPS allowed.")

    # Ensure the URL is absolute
    if not parsed.netloc:
        raise ValueError("URL must be absolute with a network location")

    # Normalise and check the domain
    domain = _normalize_domain(parsed.netloc)
    if domain not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not trusted")

    # Reconstruct the URL to ensure consistent formatting
    canonical = urlunparse(parsed._replace(fragment="", query=""))
    return canonical


# Example usage (commented out – remove comments to test):
# try:
#     print(fetch_image_url("https://cdn.safeimg.org/path/to/image.jpg"))
# except ValueError as e:
#     print(f"Validation failed: {e}")