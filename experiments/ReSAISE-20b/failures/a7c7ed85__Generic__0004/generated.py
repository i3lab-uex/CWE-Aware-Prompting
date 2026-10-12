import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (case‑insensitive)
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "flickr.com",
    "i.redd.it",
    "cdn.sstatic.net",  # Stack Exchange CDN
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def validate_image_url(img_url: str) -> str:
    """
    Validate that the given image URL belongs to a trusted domain and uses an
    allowed scheme. Return the normalized URL if valid, otherwise raise ValueError.

    Parameters:
        img_url (str): The input image URL to validate.

    Returns:
        str: The normalized, fully qualified URL if it passes validation.

    Raises:
        ValueError: If the URL's domain is not trusted or its scheme is unsupported.
    """
    if not isinstance(img_url, str):
        raise ValueError("Image URL must be a string")

    # Parse the URL
    parsed = urlparse(img_url)

    # Check scheme
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalize hostname to lower case
    host = parsed.hostname.lower() if parsed.hostname else ""
    if not host:
        raise ValueError("URL must contain a hostname")

    # Check against trusted domains
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not trusted")

    # Rebuild the URL to ensure consistent formatting
    normalized = urlunparse(
        (
            parsed.scheme.lower(),
            host,
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            parsed.fragment or "",
        )
    )

    return normalized