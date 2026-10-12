import re
from urllib.parse import urlparse, urlunparse

# Trusted image hosting providers (add more as needed)
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "unsplash.com",
    "images.unsplash.com",
    "flickr.com",
    "static.flickr.com",
    "pbs.twimg.com",
    "upload.wikimedia.org",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

def check_image_url(img_address: str) -> str:
    """
    Validate an image URL and return the fully resolved URL if it belongs to a
    trusted domain list.

    Parameters:
        img_address (str): The input image URL to validate.

    Returns:
        str: The normalized, fully resolved URL.

    Raises:
        ValueError: If the scheme is unsupported or the domain is not trusted.
    """
    if not isinstance(img_address, str):
        raise ValueError("img_address must be a string")

    # Parse the URL
    parsed = urlparse(img_address)

    # Validate scheme
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate host
    host = parsed.hostname.lower() if parsed.hostname else ""
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Check against trusted domains (exact match or subdomain)
    if not any(host == domain or host.endswith("." + domain) for domain in TRUSTED_DOMAINS):
        raise ValueError(f"Domain '{host}' is not trusted")

    # Reconstruct the URL to ensure consistency (e.g., remove fragment)
    cleaned = parsed._replace(fragment="")
    return urlunparse(cleaned)

# Example usage (for testing purposes only):
if __name__ == "__main__":
    test_urls = [
        "https://i.imgur.com/abc123.png",
        "http://unsplash.com/photos/xyz.jpg",
        "https://example.com/image.png",  # Should raise ValueError
    ]

    for url in test_urls:
        try:
            print(f"Valid URL: {check_image_url(url)}")
        except ValueError as e:
            print(f"Invalid URL: {url} -> {e}")