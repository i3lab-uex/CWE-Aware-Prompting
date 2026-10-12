import re
from urllib.parse import urlparse, ParseResult

# Pre‑approved image hosting domains (case‑insensitive)
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "picsum.photos",
    "flickr.com",
    # Add more trusted domains as needed
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def _normalize_domain(host: str) -> str:
    """
    Normalise the host component of a URL for comparison.
    Handles optional port numbers and removes trailing dots.
    """
    # Remove any trailing dot that may appear in DNS names
    host = host.rstrip(".")
    # Strip port if present
    return host.split(":")[0].lower()


def validate_image_source(img_src: str) -> str:
    """
    Validate that the provided image URL belongs to a trusted domain and
    uses an allowed scheme.

    Parameters
    ----------
    img_src : str
        The image URL to validate and resolve.

    Returns
    -------
    str
        The original URL if it passes validation checks.

    Raises
    ------
    ValueError
        If the URL has an unsupported scheme or its domain is not trusted.
    """
    if not isinstance(img_src, str):
        raise ValueError("Image source must be a string URL")

    # Parse the URL
    parsed: ParseResult = urlparse(img_src)

    # Validate scheme
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalise domain for comparison
    host = _normalize_domain(parsed.hostname or "")
    if not host:
        raise ValueError("URL does not contain a valid hostname")

    # Check against trusted domains
    if not any(host == d or host.endswith("." + d) for d in TRUSTED_DOMAINS):
        raise ValueError(f"Untrusted domain: {host}")

    # Reconstruct the URL to ensure consistency
    cleaned_url = parsed.geturl()
    return cleaned_url


# Example usage (uncomment to test):
# try:
#     print(validate_image_source("https://i.imgur.com/abcd1234.jpg"))
# except ValueError as e:
#     print(e)