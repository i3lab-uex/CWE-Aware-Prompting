import re
from urllib.parse import urlparse, ParseResult

# List of approved image hosting domains.
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "media.giphy.com",
    "i.redd.it",
}

# Allowed URL schemes.
ALLOWED_SCHEMES = {"http", "https"}


def verify_image_url(img_url: str) -> str:
    """
    Validate that an image URL belongs to a trusted domain and uses an
    allowed scheme.

    Parameters
    ----------
    img_url : str
        The URL of the image to resolve.

    Returns
    -------
    str
        The verified image URL if it passes validation.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https or if the domain is not in
        TRUSTED_DOMAINS.
    """
    # Basic sanity check: ensure input is a non-empty string
    if not isinstance(img_url, str) or not img_url.strip():
        raise ValueError("Image URL must be a non-empty string")

    parsed: ParseResult = urlparse(img_url.strip())

    # Validate scheme
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}'. Only http/https are allowed.")

    # Validate domain (netloc). Remove port if present.
    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a valid hostname")

    # Normalize to lower case for comparison
    host = host.lower()

    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not trusted")

    # Reconstruct the URL to ensure consistent formatting
    verified_url = parsed.geturl()
    return verified_url


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         print(verify_image_url("https://i.imgur.com/abc123.jpg"))
#     except ValueError as e:
#         print(f"Invalid URL: {e}")