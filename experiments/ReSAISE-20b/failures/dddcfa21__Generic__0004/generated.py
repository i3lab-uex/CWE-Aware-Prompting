import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (add or remove as needed)
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "pbs.twimg.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "flickr.com",
    "static.flickr.com",
    "i.redd.it",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def check_image_url(img_address: str) -> str:
    """
    Validate that an image URL belongs to a trusted provider.

    Parameters
    ----------
    img_address : str
        The input image URL to validate.

    Returns
    -------
    str
        The normalized, fully qualified URL if it is trusted.

    Raises
    ------
    ValueError
        If the URL scheme is unsupported, or if the domain is not in the trusted list.
    """
    # Basic sanity check: non-empty string
    if not isinstance(img_address, str) or not img_address.strip():
        raise ValueError("Image address must be a non-empty string")

    # Parse the URL
    parsed = urlparse(img_address.strip())

    # Ensure scheme is present and allowed
    if not parsed.scheme:
        raise ValueError("URL must include a scheme (http or https)")
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Extract host (netloc) and strip port if present
    netloc = parsed.netloc.split(":")[0].lower()

    # Validate domain against trusted list
    if netloc not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{netloc}' is not trusted")

    # Reconstruct the URL to ensure consistent formatting
    normalized = urlunparse(parsed._replace(scheme=parsed.scheme.lower(), netloc=netloc))

    # Basic security: ensure the path ends with an image extension
    if not re.search(r"\.(jpg|jpeg|png|gif|webp|bmp)(?:\?.*)?$", parsed.path, re.IGNORECASE):
        raise ValueError("URL does not point to a recognized image file")

    return normalized