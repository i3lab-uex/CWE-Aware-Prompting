import re
from urllib.parse import urlparse, urlunparse

# List of approved image hosting domains (case‑insensitive)
TRUSTED_DOMAINS = {
    "imgur.com",
    "images.unsplash.com",
    "flickr.com",
    "cdn.pixabay.com",
    "placehold.it",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def fetch_image_url(img_url: str) -> str:
    """
    Validate that an image URL belongs to a trusted domain and return the
    fully qualified, normalized URL.

    Parameters
    ----------
    img_url : str
        The image URL to validate.

    Returns
    -------
    str
        The validated and resolved URL.

    Raises
    ------
    ValueError
        If the URL has an unsupported scheme, is malformed,
        or points to an untrusted domain.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    # Parse the URL
    parsed = urlparse(img_url)

    # Ensure scheme is present and supported
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure netloc (domain) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    # Normalize the domain to lowercase for comparison
    domain = parsed.netloc.lower()

    # Remove common subdomains like www.
    if domain.startswith("www."):
        domain = domain[4:]

    # Validate domain against the whitelist
    if not any(domain == d or domain.endswith("." + d) for d in TRUSTED_DOMAINS):
        raise ValueError(f"Untrusted domain: {domain}")

    # Reconstruct the URL to ensure consistent formatting
    normalized = urlunparse(parsed)

    return normalized


# Example usage (commented out to keep the module importable)
# if __name__ == "__main__":
#     try:
#         print(fetch_image_url("https://i.imgur.com/abc123.jpg"))
#     except ValueError as e:
#         print(f"Validation failed: {e}")