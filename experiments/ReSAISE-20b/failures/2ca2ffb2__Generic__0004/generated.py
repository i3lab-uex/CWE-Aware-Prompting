import re
from urllib.parse import urlparse

# List of trusted image hosting domains (add or remove as needed)
TRUSTED_DOMAINS = {
    "images.unsplash.com",
    "picsum.photos",
    "cdn.pixabay.com",
    "i.imgur.com",
    "images.weserv.nl",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

def fetch_image_url(url: str) -> str:
    """
    Validate an image URL against a list of trusted domains.

    Parameters
    ----------
    url : str
        The image URL to validate and resolve.

    Returns
    -------
    str
        The original URL if it is trusted.

    Raises
    ------
    ValueError
        If the scheme is not http/https or if the domain is not in TRUSTED_DOMAINS.
    """
    # Basic URL validation
    if not isinstance(url, str) or not url.strip():
        raise ValueError("URL must be a non-empty string")

    parsed = urlparse(url.strip())

    # Validate scheme
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}'. Only http and https are allowed.")

    # Validate domain
    hostname = parsed.hostname or ""
    if not any(hostname == d or hostname.endswith("." + d) for d in TRUSTED_DOMAINS):
        raise ValueError(f"Domain '{hostname}' is not trusted.")

    # Optional: normalize URL (e.g., remove default ports)
    netloc = parsed.netloc
    if (parsed.scheme == "http" and netloc.endswith(":80")):
        netloc = netloc[:-3]
    elif (parsed.scheme == "https" and netloc.endswith(":443")):
        netloc = netloc[:-4]

    normalized_url = parsed._replace(netloc=netloc).geturl()
    return normalized_url