import re
from urllib.parse import urlparse, urlunparse

# Trusted image hosting providers (add more as needed)
_TRUSTED_DOMAINS = {
    "images.unsplash.com",
    "cdn.pixabay.com",
    "picsum.photos",
    "i.imgur.com",
    "images.weserv.nl",
    "cdn.pexels.com",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}

def _normalize_domain(domain: str) -> str:
    """
    Normalizes a domain by removing leading 'www.' and converting to lowercase.
    """
    if domain.lower().startswith("www."):
        return domain[4:].lower()
    return domain.lower()

def validate_image_url(img_url: str) -> str:
    """
    Validates that `img_url` points to a trusted image host and uses an allowed scheme.

    Parameters
    ----------
    img_url : str
        The image URL to validate.

    Returns
    -------
    str
        The original URL if it is valid.

    Raises
    ------
    ValueError
        If the URL scheme is unsupported or the domain is not in the trusted list.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    parsed = urlparse(img_url)

    # Ensure scheme is allowed
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure netloc (domain) is trusted
    domain = _normalize_domain(parsed.netloc)
    if domain not in _TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted image host: {domain}")

    # Reconstruct the URL to ensure consistency
    sanitized = urlunparse(parsed._replace(scheme=parsed.scheme.lower()))
    return sanitized

# Example usage (commented out to keep module clean)
# if __name__ == "__main__":
#     test_url = "https://images.unsplash.com/photo-12345"
#     print(validate_image_url(test_url))