import re
from urllib.parse import urlparse

# List of trusted image hosting domains.
TRUSTED_DOMAINS = [
    "imgur.com",
    "i.redd.it",
    "cdn.example.com",   # replace with real trusted domains
]

# Allowed URL schemes.
ALLOWED_SCHEMES = {"http", "https"}

def _is_trusted_domain(netloc: str) -> bool:
    """
    Check if the network location (netloc) ends with one of the trusted domains.
    The check is case‑insensitive and ignores any leading port number.
    """
    # Strip potential port
    host = netloc.split(":")[0].lower()
    return any(host == d or host.endswith("." + d) for d in TRUSTED_DOMAINS)

def verify_image_url(img_url: str) -> str:
    """
    Verify that the provided image URL belongs to a trusted domain and uses
    an allowed scheme. Returns the original URL if valid, otherwise raises
    ValueError.

    Parameters
    ----------
    img_url : str
        The URL of the image to verify.

    Returns
    -------
    str
        The verified image URL.

    Raises
    ------
    ValueError
        If the scheme is not http/https or the domain is not trusted.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    parsed = urlparse(img_url)

    # Ensure scheme is http or https
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unrecognized scheme '{parsed.scheme}'. Only HTTP/HTTPS are allowed.")

    # Ensure there is a network location
    if not parsed.netloc:
        raise ValueError("URL must contain a valid domain")

    # Verify the domain is trusted
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not trusted")

    # Reconstruct the URL to normalize it (e.g., remove default ports)
    normalized_url = parsed.geturl()

    return normalized_url