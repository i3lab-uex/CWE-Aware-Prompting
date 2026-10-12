import re
from urllib.parse import urlparse, ParseResult

# List of trusted image hosting domains. Add or remove as needed.
_TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.imghost.com",
    "pics.safe.org",
    "assets.trusted.net",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}

def _is_valid_scheme(parsed: ParseResult) -> bool:
    """Return True if the URL scheme is allowed."""
    return parsed.scheme in _ALLOWED_SCHEMES

def _is_trusted_domain(parsed: ParseResult) -> bool:
    """Return True if the netloc (domain) is in the trusted list."""
    # Normalise domain: strip port if present
    host = parsed.hostname or ""
    return host.lower() in _TRUSTED_DOMAINS

def validate_image_url(img_url: str) -> str:
    """
    Validate an image URL against a list of trusted hosting domains.

    Parameters
    ----------
    img_url : str
        The input image URL to validate.

    Returns
    -------
    str
        The original URL if it is valid and trusted.

    Raises
    ------
    ValueError
        If the URL scheme is unsupported, or the domain is not trusted.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    parsed = urlparse(img_url)

    # Basic checks
    if not _is_valid_scheme(parsed):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    if not _is_trusted_domain(parsed):
        raise ValueError(f"Domain '{parsed.netloc}' is not trusted")

    # Reconstruct the URL to ensure consistent formatting
    # (e.g., lowercasing scheme and host, removing default ports)
    normalized = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=parsed.hostname or "",
    )
    return normalized.geturl()