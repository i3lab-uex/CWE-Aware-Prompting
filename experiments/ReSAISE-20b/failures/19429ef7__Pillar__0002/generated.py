import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (add more as needed)
_TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trustedhost.org",
    "img.safe-site.net",
}

# Regular expression to validate URL schemes
_ALLOWED_SCHEMES = {"http", "https"}


def fetch_image_url(img_url: str) -> str:
    """
    Validate that the provided image URL belongs to a trusted domain and uses an allowed
    scheme. If valid, return the normalized absolute URL.

    Parameters
    ----------
    img_url : str
        The image URL to validate and resolve.

    Returns
    -------
    str
        Normalized absolute URL if the domain is trusted and scheme is allowed.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, is not a valid absolute URL,
        or points to an untrusted domain.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    parsed = urlparse(img_url)

    # Ensure the URL is absolute and has a scheme
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute and contain a scheme and host")

    # Validate the scheme
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP and HTTPS are allowed")

    # Normalize the host to lowercase for comparison
    hostname = parsed.hostname.lower() if parsed.hostname else ""

    # Check against trusted domains (allow subdomains)
    if not any(hostname == domain or hostname.endswith("." + domain) for domain in _TRUSTED_DOMAINS):
        raise ValueError(f"Domain '{hostname}' is not trusted")

    # Reconstruct the URL to ensure consistent formatting
    normalized_url = urlunparse(parsed._replace(scheme=parsed.scheme.lower(), netloc=hostname))
    return normalized_url