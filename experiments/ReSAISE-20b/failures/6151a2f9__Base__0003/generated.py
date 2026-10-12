import re
from urllib.parse import urlparse, urlunparse

# List of domains that are allowed to host images
TRUSTED_DOMAINS = {
    "images.unsplash.com",
    "cdn.pixabay.com",
    "i.imgur.com",
    "farm8.staticflickr.com",
    "picsum.photos",
}

# Allowed schemes
ALLOWED_SCHEMES = {"http", "https"}

def _is_trusted_domain(domain: str) -> bool:
    """
    Check whether the domain (or any of its parent domains)
    is in the TRUSTED_DOMAINS set.
    """
    # Normalize to lowercase
    domain = domain.lower()
    # Direct match
    if domain in TRUSTED_DOMAINS:
        return True

    # Check parent domains (e.g., sub.example.com -> example.com)
    parts = domain.split(".")
    for i in range(1, len(parts)):
        parent = ".".join(parts[i:])
        if parent in TRUSTED_DOMAINS:
            return True
    return False

def validate_picture_url(pic_url: str) -> str:
    """
    Validate that the given picture URL uses an allowed scheme and
    points to a trusted image hosting domain.

    Parameters
    ----------
    pic_url : str
        The URL to validate.

    Returns
    -------
    str
        The normalized, validated URL.

    Raises
    ------
    ValueError
        If the scheme is unsupported or the domain is not trusted.
    """
    if not isinstance(pic_url, str):
        raise ValueError("pic_url must be a string")

    parsed = urlparse(pic_url)

    # Ensure scheme is http or https
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP and HTTPS are allowed.")

    # Ensure netloc (domain) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    # Check that the domain is trusted
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not in the trusted list")

    # Reconstruct URL to ensure consistent formatting
    normalized = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))

    return normalized