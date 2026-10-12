import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (add or remove as needed)
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trusted.com",
    "img.safehost.org",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def validate_image_url(img_url: str) -> str:
    """
    Validate that an image URL belongs to a trusted domain and uses an allowed scheme.

    Parameters
    ----------
    img_url : str
        The image URL to validate.

    Returns
    -------
    str
        The original URL if it is valid.

    Raises
    ------
    ValueError
        If the scheme is unsupported or the domain is not trusted.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    # Parse the URL
    parsed = urlparse(img_url)

    # Check scheme
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Extract the domain (netloc may include port)
    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a valid hostname")

    # Normalise domain to lower case
    host = host.lower()

    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not trusted")

    # Reconstruct the URL to ensure it remains canonical
    clean_url = urlunparse(parsed)

    return clean_url