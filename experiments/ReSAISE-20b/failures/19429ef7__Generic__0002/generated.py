import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (case‑insensitive)
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "unsplash.com",
    "images.unsplash.com",
    "picsum.photos",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def _normalize_domain(domain: str) -> str:
    """
    Normalize a domain by stripping the leading 'www.' if present
    and converting to lowercase.
    """
    return domain.lower().lstrip("www.")


def fetch_image_url(img_url: str) -> str:
    """
    Validate an image URL against a list of trusted domains and
    return the fully resolved URL.

    Parameters
    ----------
    img_url : str
        The image URL to validate and resolve.

    Returns
    -------
    str
        The validated, fully resolved image URL.

    Raises
    ------
    ValueError
        If the URL has an unsupported scheme, is malformed,
        or points to an untrusted domain.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    # Parse the URL
    parsed = urlparse(img_url)

    # Validate scheme
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Validate netloc (domain)
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain)")

    domain = _normalize_domain(parsed.netloc)

    if domain not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted image hosting domain: {domain!r}")

    # Re‑assemble the URL to ensure it is canonical
    resolved = urlunparse(parsed)

    # Basic sanity check: URL must end with a common image extension
    if not re.search(r"\.(jpg|jpeg|png|gif|webp|bmp)$", parsed.path, re.IGNORECASE):
        raise ValueError("URL does not point to a recognized image file")

    return resolved