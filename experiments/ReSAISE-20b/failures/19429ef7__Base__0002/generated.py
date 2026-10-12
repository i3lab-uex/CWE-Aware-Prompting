import re
from urllib.parse import urlparse

# List of trusted image hosting domains (case‑insensitive)
TRUSTED_DOMAINS = {
    'imgur.com',
    'i.imgur.com',
    'images.unsplash.com',
    'cdn.pixabay.com',
}

# Allowed URL schemes
ALLOWED_SCHEMES = {'http', 'https'}


def fetch_image_url(img_url: str) -> str:
    """
    Validate an image URL and return the canonical URL if it belongs to a
    trusted domain. Raises ValueError otherwise.

    Args:
        img_url (str): The image URL to validate.

    Returns:
        str: The validated and resolved image URL.

    Raises:
        ValueError: If the URL is not trusted or has an unsupported scheme.
    """
    if not isinstance(img_url, str):
        raise ValueError('img_url must be a string')

    # Parse the URL
    parsed = urlparse(img_url)

    # Ensure scheme is allowed
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f'Unsupported URL scheme: {parsed.scheme}')

    # Ensure host is present
    if not parsed.hostname:
        raise ValueError('URL must contain a hostname')

    # Normalize the domain for comparison (case‑insensitive)
    host = parsed.hostname.lower()

    # Strip common subdomains like www. if desired
    # For now we consider the full host.
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f'Untrusted domain: {host}')

    # Reconstruct the URL to ensure it is canonical
    # (e.g., remove default ports)
    netloc = parsed.netloc.split(':')[0]  # drop any explicit port
    canonical_url = parsed._replace(netloc=netloc).geturl()

    # Basic sanity check: ensure the URL points to an image file
    if not re.search(r'\.(jpg|jpeg|png|gif|webp)$', parsed.path, re.IGNORECASE):
        raise ValueError('URL does not point to a recognized image file')

    return canonical_url