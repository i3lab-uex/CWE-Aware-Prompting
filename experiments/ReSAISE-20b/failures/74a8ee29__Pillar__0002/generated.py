import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (case‑insensitive)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "i.redd.it",
    "pbs.twimg.com",
    "cdn.pixabay.com",
    "staticflickr.com",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}

def check_image_link(image_link: str) -> str:
    """
    Validate an image URL against a whitelist of trusted domains and schemes.

    Parameters
    ----------
    image_link : str
        The URL to validate.

    Returns
    -------
    str
        The verified image URL if the domain is approved and scheme is valid.

    Raises
    ------
    ValueError
        If the URL does not have a recognized scheme or its domain is not trusted.
    """
    if not isinstance(image_link, str):
        raise ValueError("image_link must be a string")

    # Parse the URL
    parsed = urlparse(image_link.strip())

    # Ensure a scheme is present and allowed
    if not parsed.scheme or parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported or missing scheme: {parsed.scheme!r}")

    # Extract hostname and normalize it
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Normalize the domain (remove port if present)
    host = host.lower()

    # Check against trusted domains
    if not any(host == domain or host.endswith("." + domain) for domain in _TRUSTED_DOMAINS):
        raise ValueError(f"Untrusted host: {host!r}")

    # Reconstruct the URL to ensure no unintended components are added
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        "",  # params
        parsed.query,
        ""   # fragment
    ))

    return safe_url