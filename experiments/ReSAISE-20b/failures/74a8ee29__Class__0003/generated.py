import re
from urllib.parse import urlparse

# List of domains that are considered trustworthy for hosting images.
TRUSTED_DOMAINS = {
    "imgur.com",
    "flickr.com",
    "cdn.pixabay.com",
    "picsum.photos",
    "unsplash.com",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

def _normalize_domain(netloc: str) -> str:
    """
    Strip optional port and leading 'www.' from a netloc string.
    """
    # Remove port if present
    domain = netloc.split(":")[0]
    # Strip leading 'www.'
    return re.sub(r"^www\.", "", domain, flags=re.IGNORECASE)

def check_image_link(image_link: str) -> str:
    """
    Validate that *image_link* points to a trusted image hosting domain
    and uses an allowed URL scheme.

    Parameters
    ----------
    image_link : str
        The URL of the image to verify.

    Returns
    -------
    str
        The original *image_link* if it is trusted and well‑formed.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        or does not belong to a trusted domain.
    """
    if not isinstance(image_link, str):
        raise ValueError("image_link must be a string")

    parsed = urlparse(image_link)

    # Scheme validation
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Domain validation
    domain = _normalize_domain(parsed.netloc.lower())
    if domain not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not trusted")

    # Basic sanity check: path should end with an image extension
    if not re.search(r"\.(png|jpe?g|gif|webp)$", parsed.path, re.IGNORECASE):
        raise ValueError("URL does not point to a recognized image file")

    # No network I/O is performed here – we simply return the original URL.
    # This avoids acting as a proxy or unintentionally following redirects,
    # mitigating CWE‑441 (Confused Deputy).
    return image_link