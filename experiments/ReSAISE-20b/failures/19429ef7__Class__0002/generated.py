import re
from urllib.parse import urlparse, ParseResult

# List of trusted image hosting domains (case‑insensitive)
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "picsum.photos",
    "cdn.pixabay.com",
    "flickr.com",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def fetch_image_url(img_url: str) -> str:
    """
    Validate that *img_url* points to a trusted image hosting domain and has an
    allowed scheme.  Return the fully resolved URL unchanged if it passes all
    checks.

    Parameters
    ----------
    img_url : str
        The image URL to check and resolve.

    Returns
    -------
    str
        The validated URL unchanged.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, has a missing host component,
        or does not belong to one of the trusted domains.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    # Parse the URL and ensure it has a scheme and netloc
    parsed: ParseResult = urlparse(img_url)
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    if not parsed.netloc:
        raise ValueError("URL must contain a host component")

    # Normalize the domain to lowercase and strip port if present
    netloc = parsed.netloc.split(":")[0].lower()

    # Verify the domain is in the trusted list
    if netloc not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {netloc}")

    # Reconstruct the URL to avoid any subtle manipulation
    # (e.g., a user might provide an encoded slash that changes the host)
    sanitized_url = parsed.geturl()

    # Basic sanity check: ensure no relative paths that might cause confusion
    if not re.match(r"^https?://", sanitized_url, flags=re.IGNORECASE):
        raise ValueError("URL must start with http:// or https://")

    return sanitized_url