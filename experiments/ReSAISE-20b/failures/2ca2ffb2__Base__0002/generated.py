import re
from urllib.parse import urlparse, urlunparse

# A list of trusted image hosting domains (case‑insensitive)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "flickr.com",
    "cdn.example.com",
    "images.unsplash.com",
}

# Allowed schemes
_ALLOWED_SCHEMES = {"http", "https"}

def _is_trusted_domain(host: str) -> bool:
    """
    Return True if the host ends with one of the trusted domains.
    This allows subdomains like `i.imgur.com` to be accepted.
    """
    host = host.lower()
    return any(host == domain or host.endswith("." + domain) for domain in _TRUSTED_DOMAINS)

def fetch_image_url(url: str) -> str:
    """
    Resolve an image URL and ensure that it points to a trusted domain.

    Parameters
    ----------
    url : str
        The original image URL.

    Returns
    -------
    str
        The normalized URL that has been verified to point to a trusted domain.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https, or if the domain is not trusted.
    """
    # Parse the URL
    parsed = urlparse(url)

    # Validate scheme
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Validate host
    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted host: {parsed.netloc!r}")

    # Re‑build the URL to ensure no stray fragments or query parameters
    safe_parts = (
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        "",  # params
        "",  # query
        ""   # fragment
    )
    return urlunparse(safe_parts)