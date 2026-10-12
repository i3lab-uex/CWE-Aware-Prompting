import re
from urllib.parse import urlparse, urlunparse

# List of trusted image host domains.
_TRUSTED_DOMAINS = {
    "i.imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "picsum.photos",
    "flickr.com",
    "upload.wikimedia.org",
    # Add more trusted domains as needed
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}


def _normalize_domain(domain: str) -> str:
    """
    Normalise domain names by stripping leading/trailing whitespace
    and converting to lowercase.
    """
    return domain.strip().lower()


def check_image_url(img_address: str) -> str:
    """
    Validate an image URL against a list of trusted domains and supported schemes.

    Parameters
    ----------
    img_address : str
        The image URL to validate.

    Returns
    -------
    str
        The original URL if it is valid and belongs to a trusted domain.

    Raises
    ------
    ValueError
        If the URL scheme is unsupported, or the domain is not trusted.
    """
    if not isinstance(img_address, str):
        raise ValueError("Image address must be a string")

    # Parse the URL
    parsed = urlparse(img_address)

    # Validate scheme
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate domain
    netloc = _normalize_domain(parsed.netloc)
    if not any(netloc == d or netloc.endswith("." + d) for d in _TRUSTED_DOMAINS):
        raise ValueError(f"Domain '{netloc}' is not trusted")

    # Rebuild the URL to ensure consistency
    cleaned = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=netloc,
    )
    return urlunparse(cleaned)


# Example usage (commented out for production use)
if __name__ == "__main__":
    test_urls = [
        "https://i.imgur.com/abc123.png",
        "http://cdn.pixabay.com/photo/2020/01/01/12/00/abc.jpg",
        "https://example.com/image.png",  # Should raise ValueError
    ]

    for url in test_urls:
        try:
            print(f"Valid: {check_image_url(url)}")
        except ValueError as e:
            print(f"Invalid: {e}")