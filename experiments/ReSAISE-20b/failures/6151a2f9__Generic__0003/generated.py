import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains. Adjust as needed.
_TRUSTED_DOMAINS = {
    "images.unsplash.com",
    "cdn.pixabay.com",
    "i.imgur.com",
    "res.cloudinary.com",
    "picsum.photos",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}

def _is_trusted_domain(host: str) -> bool:
    """
    Check if the host is exactly one of the trusted domains or a sub‑domain
    of one.  This prevents attacks like ``evil.com/images.unsplash.com``.
    """
    host = host.lower()
    if host in _TRUSTED_DOMAINS:
        return True
    # Allow subdomains only if the base domain is trusted.
    for domain in _TRUSTED_DOMAINS:
        if host.endswith("." + domain):
            return True
    return False

def validate_picture_url(pic_url: str) -> str:
    """
    Validate an image URL.

    Parameters
    ----------
    pic_url : str
        The input image URL to validate.

    Returns
    -------
    str
        The fully resolved, canonical URL if it is trusted and uses an
        allowed scheme.

    Raises
    ------
    ValueError
        If the URL has an unsupported scheme, is malformed, or its domain
        is not in the trusted list.
    """
    if not isinstance(pic_url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(pic_url)

    # Scheme must be http or https
    if parsed.scheme not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Host must be present
    if not parsed.netloc:
        raise ValueError("URL missing host component")

    # Validate domain
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted host: {parsed.netloc}")

    # Reconstruct the URL to ensure canonical form
    cleaned = urlunparse((
        parsed.scheme,
        parsed.netloc.lower(),
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))
    return cleaned