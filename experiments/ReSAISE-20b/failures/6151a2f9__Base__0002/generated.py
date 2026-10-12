import re
from urllib.parse import urlparse

# List of trusted image hosting providers (example domains)
TRUSTED_DOMAINS = {
    "imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "i.redd.it",
    "flickr.com",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

def _is_trusted_domain(netloc: str) -> bool:
    """
    Check if the netloc (domain part of URL) matches any trusted domain.
    Supports subdomains by ensuring the domain ends with a trusted domain
    and that the preceding character is a dot or start of string.
    """
    netloc = netloc.lower()
    for domain in TRUSTED_DOMAINS:
        # Exact match
        if netloc == domain.lower():
            return True
        # Subdomain check: endswith + preceding dot
        if netloc.endswith("." + domain.lower()):
            return True
    return False

def validate_picture_url(pic_url: str) -> str:
    """
    Validate that a given picture URL belongs to one of the trusted image
    hosting providers and uses an allowed scheme.

    Parameters
    ----------
    pic_url : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it is valid and trusted.

    Raises
    ------
    ValueError
        If the URL scheme is unsupported or the domain is not trusted.
    """
    if not isinstance(pic_url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(pic_url)

    # Scheme validation
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Domain validation
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.netloc}")

    # Optional: ensure the path ends with an image extension
    if not re.search(r"\.(jpg|jpeg|png|gif|webp)$", parsed.path, re.IGNORECASE):
        raise ValueError("URL does not point to a recognized image format")

    return pic_url