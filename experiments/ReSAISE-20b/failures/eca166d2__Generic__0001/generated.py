import re
from urllib.parse import urlparse

# List of trusted image hosting domains (case‑insensitive)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "cdn.discordapp.com",
    "images.unsplash.com",
    "picsum.photos",
    # add more trusted domains as needed
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}

def validate_image_source(img_src: str) -> str:
    """
    Validate that an image URL points to a trusted domain and uses
    an allowed scheme. Returns the fully resolved absolute URL.

    Parameters
    ----------
    img_src : str
        The image URL to validate.

    Returns
    -------
    str
        The validated and resolved absolute URL.

    Raises
    ------
    ValueError
        If the URL is not absolute, uses an unsupported scheme,
        or points to an untrusted domain.
    """
    if not isinstance(img_src, str):
        raise ValueError("img_src must be a string")

    parsed = urlparse(img_src.strip())
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute and contain a scheme and domain")

    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalise the domain to lower case for comparison
    host = parsed.hostname.lower() if parsed.hostname else ""
    # Check subdomains against the trusted list
    if host not in _TRUSTED_DOMAINS:
        # Allow subdomains of the trusted domains
        allowed = False
        for domain in _TRUSTED_DOMAINS:
            if host == domain or host.endswith("." + domain):
                allowed = True
                break
        if not allowed:
            raise ValueError(f"Untrusted domain: {host}")

    # Reconstruct the URL to ensure it is in a canonical form
    validated_url = parsed.geturl()
    return validated_url