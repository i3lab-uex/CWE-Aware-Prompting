import re
from urllib.parse import urlparse

# List of trusted image hosting providers
TRUSTED_DOMAINS = {
    "images.unsplash.com",
    "cdn.pixabay.com",
    "images.pexels.com",
    "i.imgur.com",
    "cdn.jsdelivr.net",   # e.g., for static images
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

def validate_image_url(img_url: str) -> str:
    """
    Validate that the supplied image URL belongs to a trusted domain and uses
    an allowed scheme. The function does not fetch the resource; it merely
    performs a structural check.

    Parameters:
        img_url (str): The image URL to validate.

    Returns:
        str: The original URL if it passes validation.

    Raises:
        ValueError: If the URL is malformed, uses an unsupported scheme,
                    or its domain is not in the trusted list.
    """
    if not isinstance(img_url, str):
        raise ValueError("Image URL must be a string")

    # Parse the URL
    parsed = urlparse(img_url)

    # Validate scheme
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Validate domain
    hostname = parsed.hostname or ""
    if not any(hostname == domain or hostname.endswith("." + domain) for domain in TRUSTED_DOMAINS):
        raise ValueError(f"Untrusted host: {hostname!r}")

    # Basic sanity check for path
    if not parsed.path or re.search(r"\.\.\/", parsed.path):
        raise ValueError("URL path is invalid or contains directory traversal")

    # All checks passed – return the original URL
    return img_url