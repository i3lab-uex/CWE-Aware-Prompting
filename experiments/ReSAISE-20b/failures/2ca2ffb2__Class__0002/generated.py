import re
from urllib.parse import urlparse

# List of trusted image hosting domains.
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trusted.com",
    "static.safehost.org",
}

# Allowed URL schemes.
ALLOWED_SCHEMES = {"http", "https"}


def fetch_image_url(url: str) -> str:
    """
    Resolve an image URL and ensure it points to a trusted domain.

    Parameters
    ----------
    url : str
        The original image URL to validate.

    Returns
    -------
    str
        The verified image URL if the domain is approved.

    Raises
    ------
    ValueError
        If the URL scheme is unrecognized, if the domain is not trusted,
        or if the URL cannot be parsed.
    """
    # Basic sanity check: non-empty string
    if not isinstance(url, str) or not url.strip():
        raise ValueError("URL must be a non-empty string")

    # Parse the URL
    try:
        parsed = urlparse(url.strip())
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to parse URL: {exc}") from exc

    # Validate scheme
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate netloc (domain)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid host")

    # Normalize the hostname for comparison
    hostname = hostname.lower()

    # Ensure the domain matches one of the trusted domains.
    # We allow subdomains by checking the suffix.
    if not any(hostname == td or hostname.endswith("." + td) for td in TRUSTED_DOMAINS):
        raise ValueError(f"Domain '{hostname}' is not trusted")

    # Reconstruct the URL to avoid any hidden components (e.g., IPv6 addresses)
    safe_url = parsed.geturl()
    return safe_url