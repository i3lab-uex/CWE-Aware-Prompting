import re
from urllib.parse import urlparse, urljoin

# Whitelisted image hosting domains (add or remove as needed)
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "picsum.photos",
    "images.unsplash.com",
    "cdn.pixabay.com",
}

# Supported URL schemes
SUPPORTED_SCHEMES = {"http", "https"}


def _is_trusted_domain(netloc: str) -> bool:
    """
    Check if the netloc (hostname with optional port) belongs to a trusted domain.
    """
    # Remove any port number
    host = netloc.split(":")[0].lower()
    # Check direct match or subdomain of a trusted domain
    for domain in TRUSTED_DOMAINS:
        if host == domain or host.endswith("." + domain):
            return True
    return False


def fetch_image_url(img_url: str) -> str:
    """
    Validate that `img_url` points to a trusted image hosting domain and return
    the fully resolved absolute URL.

    Parameters
    ----------
    img_url : str
        The image URL to validate and resolve.

    Returns
    -------
    str
        The validated, absolute URL.

    Raises
    ------
    ValueError
        If the URL has an unsupported scheme or points to an untrusted domain.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    parsed = urlparse(img_url)

    # Ensure scheme is present and supported
    if parsed.scheme.lower() not in SUPPORTED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure we have a network location
    if not parsed.netloc:
        raise ValueError("URL must contain a network location")

    # Validate domain
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.netloc}")

    # Resolve relative URLs (if any) against the provided URL
    absolute_url = urljoin(img_url, parsed.path)

    # Reconstruct the URL with original scheme and netloc
    resolved = absolute_url
    if parsed.query:
        resolved += f"?{parsed.query}"
    if parsed.fragment:
        resolved += f"#{parsed.fragment}"

    return resolved