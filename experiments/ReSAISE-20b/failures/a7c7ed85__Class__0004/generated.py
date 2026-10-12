import re
from urllib.parse import urlparse, urlunparse

# List of fully qualified domain names that are considered trustworthy.
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "unsplash.com",
    "images.unsplash.com",
    "picsum.photos",
    "cdn.pixabay.com",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

def _normalize_domain(domain: str) -> str:
    """
    Normalise a domain for comparison.
    - Lowercase
    - Remove leading 'www.'
    """
    domain = domain.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    return domain

def validate_image_url(img_url: str) -> str:
    """
    Validate that the given image URL points to a trusted domain and uses an allowed scheme.

    Parameters
    ----------
    img_url : str
        The URL to validate.

    Returns
    -------
    str
        The original, fully resolved URL if it is valid.

    Raises
    ------
    ValueError
        If the URL's scheme is not supported or its domain is not in the trusted list.
    """
    if not isinstance(img_url, str):
        raise ValueError("Image URL must be a string")

    # Parse the URL
    parsed = urlparse(img_url)

    # Check scheme
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure the netloc (domain) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    # Normalise the domain
    domain = _normalize_domain(parsed.netloc)

    # Validate against trusted domains
    if domain not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not trusted")

    # Reconstruct the URL to ensure it has no fragments or query parameters that might be
    # maliciously used in a request. We keep path, params, query, fragment as is,
    # but strip any leading/trailing whitespace.
    cleaned = parsed._replace(
        path=parsed.path.strip(),
        params=parsed.params.strip(),
        query=parsed.query.strip(),
        fragment=parsed.fragment.strip()
    )
    return urlunparse(cleaned)

# Example usage (commented out):
# try:
#     safe_url = validate_image_url("https://i.imgur.com/abcd1234.jpg")
#     print(safe_url)
# except ValueError as e:
#     print(f"Invalid image URL: {e}")