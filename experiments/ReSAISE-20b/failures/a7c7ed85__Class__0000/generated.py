import re
from urllib.parse import urlparse

# List of trusted image hosting domains.
TRUSTED_DOMAINS = {
    "images.unsplash.com",
    "picsum.photos",
    "cdn.example.com",  # replace with your own trusted domains
}

# Allowed URL schemes.
ALLOWED_SCHEMES = {"http", "https"}

def validate_image_url(img_url: str) -> str:
    """
    Validate an image URL and return the original URL if it is from a trusted
    domain and uses an allowed scheme.

    Parameters:
        img_url (str): The image URL to validate.

    Returns:
        str: The validated, original URL.

    Raises:
        ValueError: If the scheme is not allowed or the domain is not trusted.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    # Parse the URL.
    parsed = urlparse(img_url)

    # Validate scheme.
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate domain.
    netloc = parsed.netloc.lower()
    # Remove port if present (e.g., example.com:443).
    domain = re.sub(r":\d+$", "", netloc)

    if domain not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted image host: {domain}")

    # Return the original URL unchanged.
    return img_url