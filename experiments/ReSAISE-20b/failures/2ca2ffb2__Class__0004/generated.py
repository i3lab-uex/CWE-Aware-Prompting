import re
from urllib.parse import urlparse, ParseResult

# List of trusted image hosting domains (case‑insensitive)
_TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trustedsite.org",
    "pics.safehost.net",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}


def fetch_image_url(url: str) -> str:
    """
    Resolve and verify an image URL.

    Parameters
    ----------
    url : str
        The original image URL to be validated.

    Returns
    -------
    str
        The verified, final image URL if it belongs to a trusted domain.

    Raises
    ------
    ValueError
        If the URL's scheme is not allowed, or if its hostname does not match a
        trusted domain. The function also raises ValueError for malformed URLs.
    """
    if not isinstance(url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed: ParseResult = urlparse(url)

    # Validate scheme
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate hostname
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Normalize to lowercase for comparison
    host_lower = host.lower()

    # Check if the hostname ends with any trusted domain (subdomain allowed)
    if not any(host_lower == d or host_lower.endswith("." + d) for d in _TRUSTED_DOMAINS):
        raise ValueError(f"Untrusted domain: {host}")

    # Reconstruct the URL to ensure it is well‑formed
    cleaned_url = parsed.geturl()
    return cleaned_url


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     try:
#         print(fetch_image_url("https://cdn.trustedsite.org/path/to/image.jpg"))
#     except ValueError as e:
#         print(f"Validation error: {e}")