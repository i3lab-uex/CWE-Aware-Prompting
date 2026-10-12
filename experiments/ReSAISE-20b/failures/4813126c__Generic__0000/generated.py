import re
from urllib.parse import urlparse

import requests


# List of trusted image hosting domains (case‑insensitive)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "picsum.photos",
    "flickr.com",
    "static.flickr.com",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}


def _is_trusted_domain(domain: str) -> bool:
    """Return True if the domain (or any of its parent domains) is trusted."""
    # Normalise to lowercase
    domain = domain.lower()
    return any(
        domain == trusted or domain.endswith("." + trusted)
        for trusted in _TRUSTED_DOMAINS
    )


def verify_image_url(img_url: str) -> str:
    """
    Resolve an image URL and return the final destination only if it points to a trusted
    domain.

    Parameters
    ----------
    img_url : str
        The original URL to validate and resolve.

    Returns
    -------
    str
        The final resolved image URL if the domain is trusted.

    Raises
    ------
    ValueError
        If the scheme is not HTTP/HTTPS, or if the final resolved domain is not trusted.
    """
    # Basic validation
    parsed = urlparse(img_url)
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unrecognized URL scheme: {parsed.scheme!r}")

    # Resolve redirects to obtain the final URL
    try:
        resp = requests.get(img_url, allow_redirects=True, timeout=10)
        final_url = resp.url
    except requests.RequestException as exc:
        raise ValueError(f"Failed to resolve URL: {exc}") from exc

    final_parsed = urlparse(final_url)
    if not _is_trusted_domain(final_parsed.hostname or ""):
        raise ValueError(f"Domain {final_parsed.hostname!r} is not trusted")

    return final_url