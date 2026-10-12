import re
from urllib.parse import urlparse, urlunparse

# List of approved image hosting domains (case‑insensitive)
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "storage.googleapis.com",
    "s3.amazonaws.com",  # optional: specific bucket names could be added
}

# Allowed schemes
ALLOWED_SCHEMES = {"http", "https"}

def _is_private_ip(ip: str) -> bool:
    """
    Quick check for private IP ranges to mitigate SSRF via IP addresses.
    Returns True if the IP is in a private or reserved range.
    """
    # Simple regexes for IPv4 private ranges
    if re.match(r"^(10\.|192\.168\.|172\.(1[6-9]|2\d|3[0-1])\.)", ip):
        return True
    # RFC 1918 and other reserved ranges (IPv6 omitted for brevity)
    return False

def get_image_link(link_image: str) -> str:
    """
    Validate that a given image URL belongs to an approved host and
    return the fully resolved URL.

    Args:
        link_image (str): The image URL to validate.

    Returns:
        str: The validated and resolved URL.

    Raises:
        ValueError: If the URL is malformed, uses an unsupported scheme,
                    or points to an untrusted domain.
    """
    if not isinstance(link_image, str):
        raise ValueError("link_image must be a string")

    parsed = urlparse(link_image)

    # Ensure scheme is allowed
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalise netloc (remove default ports)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid host")

    # Reject private IP addresses (SSRF mitigation)
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", hostname) and _is_private_ip(hostname):
        raise ValueError("URL points to a private IP address")

    # Check domain against whitelist (case‑insensitive)
    if hostname.lower() not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted host: {hostname}")

    # Reconstruct the URL to ensure it is canonical
    cleaned = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=hostname,
        params="",
        query="",
        fragment=""
    )
    return urlunparse(cleaned)