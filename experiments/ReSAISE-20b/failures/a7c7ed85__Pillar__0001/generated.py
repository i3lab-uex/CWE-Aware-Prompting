import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting providers (example domains)
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "picsum.photos",
    "upload.wikimedia.org",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def validate_image_url(img_url: str) -> str:
    """
    Validate that an image URL belongs to a trusted provider and uses
    a supported scheme.

    Parameters
    ----------
    img_url : str
        The input image URL to validate.

    Returns
    -------
    str
        The fully resolved, validated URL.

    Raises
    ------
    ValueError
        If the URL is malformed, has an unsupported scheme,
        or its domain is not in the trusted list.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    # Parse the URL
    parsed = urlparse(img_url)

    # Basic validation of scheme and netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL: missing scheme or host")

    # Scheme must be http or https
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Normalize domain (lowercase) and strip any port
    host = parsed.hostname.lower() if parsed.hostname else ""
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Check against trusted domains
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {host}")

    # Reconstruct the URL to ensure it is fully qualified
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))

    # Additional security check: ensure no relative paths like ".."
    if re.search(r"/\.\./", sanitized):
        raise ValueError("URL contains unsafe path traversal")

    return sanitized