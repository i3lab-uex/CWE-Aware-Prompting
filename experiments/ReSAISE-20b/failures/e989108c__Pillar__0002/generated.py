import re
from urllib.parse import urlparse

# List of trusted image hosting domains (add or remove as needed)
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "flickr.com",
    "upload.wikimedia.org",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def get_image_link(link_image: str) -> str:
    """
    Validate that *link_image* points to a trusted image hosting domain
    and uses an allowed scheme (http or https).  The function returns the
    original URL unchanged if it passes validation.

    Parameters
    ----------
    link_image : str
        The image URL to validate and resolve.

    Returns
    -------
    str
        The validated, fully-qualified image URL.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme or points to an untrusted domain.
    """
    if not isinstance(link_image, str):
        raise ValueError("link_image must be a string")

    # Parse the URL
    parsed = urlparse(link_image)

    # Check scheme
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalize netloc (strip port if present)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # For IPv6 addresses, strip brackets
    host = host.lower()

    # Verify domain is in the trusted list (exact match or subdomain)
    if host not in TRUSTED_DOMAINS:
        # Allow subdomains of trusted domains
        for domain in TRUSTED_DOMAINS:
            if host.endswith("." + domain):
                break
        else:
            raise ValueError(f"Untrusted domain: {host}")

    # Reconstruct the URL to ensure consistency
    return parsed.geturl()