import re
from urllib.parse import urlparse, ParseResult

# List of trusted image hosting domains (exact match or subdomain)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "picsum.photos",
    # Add more trusted domains here
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}


def _is_trusted_domain(host: str) -> bool:
    """
    Check whether the given host is a trusted domain or sub‑domain of one.
    """
    # Normalise host (lowercase, strip trailing dot)
    host = host.lower().rstrip(".")
    for domain in _TRUSTED_DOMAINS:
        if host == domain or host.endswith("." + domain):
            return True
    return False


def fetch_image_url(url: str) -> str:
    """
    Resolve and validate an image URL.

    Parameters
    ----------
    url : str
        The original image URL to validate.

    Returns
    -------
    str
        The validated image URL if the domain and scheme are trusted.

    Raises
    ------
    ValueError
        If the URL is malformed, has an unrecognized scheme,
        or its domain is not in the list of trusted domains.
    """
    if not isinstance(url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed: ParseResult = urlparse(url)

    # Validate scheme
    if parsed.scheme not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate host
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (host)")

    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted host: {parsed.netloc}")

    # Reconstruct the URL to ensure it is normalized
    # This also strips any fragments and query parameters that might be used maliciously.
    safe_url = parsed._replace(fragment="", query="").geturl()

    return safe_url