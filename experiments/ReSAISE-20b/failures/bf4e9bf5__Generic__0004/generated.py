import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (add or remove as needed)
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.safehost.org",
    "pics.trusted.net",
}

def resolve_image_url(image_url: str) -> str:
    """
    Resolve and validate an image URL against a list of trusted domains.

    Parameters
    ----------
    image_url : str
        The image URL to be validated and returned.

    Returns
    -------
    str
        The normalized, validated image URL.

    Raises
    ------
    ValueError
        If the domain of ``image_url`` is not in the trusted list.
    """
    if not isinstance(image_url, str):
        raise TypeError("image_url must be a string")

    # Parse the URL
    parsed = urlparse(image_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {image_url!r}")

    # Normalize the domain to lowercase for comparison
    domain = parsed.netloc.lower()

    # Remove default ports (e.g., :80, :443) for accurate comparison
    domain = re.sub(r":(80|443)$", "", domain)

    if domain not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {domain!r}")

    # Reconstruct the URL to ensure consistent formatting
    normalized = urlunparse(parsed._replace(scheme=parsed.scheme.lower()))

    return normalized