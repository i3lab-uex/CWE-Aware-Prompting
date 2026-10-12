import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (case‑insensitive)
TRUSTED_DOMAINS = {
    "imgur.com",
    "flickr.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "pbs.twimg.com",
    "i.redd.it",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def _is_trusted_domain(netloc: str) -> bool:
    """
    Check if the given network location (netloc) matches one of the trusted domains.
    Subdomains are allowed as long as they end with a trusted domain.
    """
    netloc = netloc.lower()
    for domain in TRUSTED_DOMAINS:
        # Exact match or subdomain
        if netloc == domain or netloc.endswith("." + domain):
            return True
    return False


def check_image_url(img_address: str) -> str:
    """
    Validate that *img_address* points to a trusted image hosting provider.

    Parameters
    ----------
    img_address : str
        The URL to validate.

    Returns
    -------
    str
        The canonical, validated URL.

    Raises
    ------
    ValueError
        If the URL's scheme is not HTTP(S) or if its domain is untrusted.
    """
    # Basic sanity check
    if not isinstance(img_address, str):
        raise ValueError("img_address must be a string")

    # Parse the URL
    parsed = urlparse(img_address)

    # Validate scheme
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Validate domain
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain)")

    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.netloc!r}")

    # Reconstruct the URL to normalize it (remove fragments, etc.)
    cleaned = parsed._replace(fragment="", query="")
    canonical_url = urlunparse(cleaned)

    return canonical_url