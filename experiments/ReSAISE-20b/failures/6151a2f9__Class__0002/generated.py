import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (example list)
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "picsum.photos",
    "cdn.pixabay.com",
    "flickr.com",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def _normalize_domain(domain: str) -> str:
    """
    Normalizes the domain by stripping leading 'www.' and converting to lowercase.
    """
    return domain.lower().lstrip("www.")


def validate_picture_url(pic_url: str) -> str:
    """
    Validates that a picture URL is from a trusted image host.

    Parameters
    ----------
    pic_url : str
        The input picture URL to validate.

    Returns
    -------
    str
        The normalized, fully-qualified URL if it is trusted.

    Raises
    ------
    ValueError
        If the scheme is unsupported or the domain is not trusted.
    """
    if not isinstance(pic_url, str):
        raise ValueError("pic_url must be a string")

    # Parse the URL
    parsed = urlparse(pic_url)

    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain)")

    # Normalize domain
    normalized_domain = _normalize_domain(parsed.netloc)

    if normalized_domain not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain {normalized_domain!r} is not trusted")

    # Rebuild the URL to ensure consistency (e.g., remove default ports)
    cleaned = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=normalized_domain,
    )
    return urlunparse(cleaned)


# Example usage (for testing purposes only)
if __name__ == "__main__":
    test_urls = [
        "https://i.imgur.com/abcd1234.jpg",
        "http://www.images.unsplash.com/photo-1234567890",
        "https://example.com/image.png",  # should raise
    ]

    for url in test_urls:
        try:
            print(f"Valid URL: {validate_picture_url(url)}")
        except ValueError as e:
            print(f"Invalid URL: {url} -> {e}")