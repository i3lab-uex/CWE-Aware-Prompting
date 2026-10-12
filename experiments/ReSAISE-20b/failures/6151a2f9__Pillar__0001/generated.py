import re
from urllib.parse import urlparse, ParseResult

# List of trusted image hosting providers (domain names)
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "picsum.photos",
    "flickr.com",
    # add more trusted domains as needed
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def _is_valid_domain(domain: str) -> bool:
    """
    Check if the given domain (or any of its parent domains) is in the trusted list.
    """
    # Normalize by removing leading 'www.' if present
    domain = domain.lower()
    if domain.startswith("www."):
        domain = domain[4:]

    # Direct match
    if domain in TRUSTED_DOMAINS:
        return True

    # Check parent domains (e.g., subdomain.example.com)
    parts = domain.split(".")
    for i in range(1, len(parts)):
        parent = ".".join(parts[i:])
        if parent in TRUSTED_DOMAINS:
            return True
    return False


def validate_picture_url(pic_url: str) -> str:
    """
    Validate that an image URL belongs to a trusted domain and uses
    an allowed scheme. Returns the original URL if valid, otherwise raises ValueError.

    Parameters:
        pic_url (str): The input image URL.

    Returns:
        str: The validated, fully-qualified image URL.

    Raises:
        ValueError: If the scheme is unsupported or the domain is not trusted.
    """
    if not isinstance(pic_url, str):
        raise ValueError("pic_url must be a string")

    # Parse the URL
    parsed: ParseResult = urlparse(pic_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL format")

    # Scheme check
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Domain check
    if not _is_valid_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.netloc}")

    # Reconstruct the URL to ensure normalization
    normalized_url = parsed.geturl()
    return normalized_url


# Example usage (commented out to avoid accidental execution)
# if __name__ == "__main__":
#     try:
#         valid_url = validate_picture_url("https://i.imgur.com/abcd1234.png")
#         print(f"Valid URL: {valid_url}")
#     except ValueError as e:
#         print(f"Validation error: {e}")