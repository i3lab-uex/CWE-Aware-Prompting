import re
from urllib.parse import urlparse

# List of trusted image hosting domains (add or remove as needed)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "flickr.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "pbs.twimg.com",   # Twitter images
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}


def fetch_image_url(url: str) -> str:
    """
    Validate that a given image URL belongs to one of the trusted domains and uses an
    allowed scheme. If valid, return the original URL unchanged; otherwise raise a
    ValueError.

    Parameters
    ----------
    url : str
        The URL of the image to resolve.

    Returns
    -------
    str
        The verified image URL.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme, or does not belong to a
        trusted domain.
    """
    if not isinstance(url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(url)

    # Ensure scheme is present and allowed
    if not parsed.scheme:
        raise ValueError("URL must contain a scheme (http or https)")
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure netloc (domain) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain)")

    # Normalise the domain to lowercase for comparison
    hostname = parsed.hostname.lower() if parsed.hostname else ""

    # Check that the domain ends with one of the trusted domains.
    # This allows subdomains (e.g., i.imgur.com) while preventing
    # domain spoofing via unrelated subdomains.
    if not any(hostname == trusted or hostname.endswith("." + trusted)
               for trusted in _TRUSTED_DOMAINS):
        raise ValueError(f"Domain '{hostname}' is not trusted")

    # Optional: Validate the path ends with a typical image file extension.
    # This is not strictly required but helps guard against URLs that point
    # to non-image resources on a trusted domain.
    if not re.search(r"\.(jpg|jpeg|png|gif|bmp|webp)(\?.*)?$", parsed.path, re.IGNORECASE):
        raise ValueError("URL does not point to a recognized image file")

    # All checks passed; return the original URL
    return url