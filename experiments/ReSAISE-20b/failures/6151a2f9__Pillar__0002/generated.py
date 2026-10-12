import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (case‑insensitive)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "picsum.photos",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}


def _is_trusted_domain(domain: str) -> bool:
    """Check if the domain is in the trusted list."""
    return domain.lower() in _TRUSTED_DOMAINS


def validate_picture_url(pic_url: str) -> str:
    """
    Validate that the supplied picture URL uses a supported scheme
    and points to one of the trusted image hosting providers.

    Parameters
    ----------
    pic_url : str
        The input picture URL to validate.

    Returns
    -------
    str
        The fully qualified, validated URL.

    Raises
    ------
    ValueError
        If the scheme is unsupported or the domain is not trusted.
    """
    if not isinstance(pic_url, str):
        raise ValueError("pic_url must be a string")

    parsed = urlparse(pic_url)

    # Scheme validation
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Domain validation
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.netloc!r}")

    # Re‑build the URL to ensure normalisation (e.g., missing trailing slash)
    cleaned_url = urlunparse(parsed)

    # Optional: ensure the URL ends with a common image extension
    if not re.search(r"\.(jpg|jpeg|png|gif|webp)$", parsed.path, re.IGNORECASE):
        raise ValueError("URL does not point to a recognised image file")

    return cleaned_url