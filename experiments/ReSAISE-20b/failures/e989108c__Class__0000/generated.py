import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (case‑insensitive)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "flickr.com",
    # add more domains as needed
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}

def get_image_link(link_image: str) -> str:
    """
    Validate that *link_image* is a URL pointing to an image hosted on one of the
    pre‑approved domains and return the fully resolved URL.

    Parameters
    ----------
    link_image : str
        The image URL to validate and resolve.

    Returns
    -------
    str
        The validated and resolved URL (unchanged if already fully qualified).

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, does not resolve to a trusted domain,
        or is malformed.
    """
    if not isinstance(link_image, str):
        raise ValueError("link_image must be a string")

    # Parse the URL
    parsed = urlparse(link_image)

    # Ensure scheme is http or https
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Extract the host (netloc) and normalize it
    host = parsed.hostname.lower() if parsed.hostname else ""
    if not host:
        raise ValueError("URL must contain a hostname")

    # Validate domain against the whitelist
    if host not in _TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {host!r}")

    # Reconstruct the URL to ensure it is in a canonical form
    cleaned = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))

    return cleaned