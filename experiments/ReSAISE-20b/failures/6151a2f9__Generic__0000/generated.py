import re
from urllib.parse import urlparse, ParseResult

# List of trusted image hosting domains (add or remove as needed)
TRUSTED_DOMAINS = {
    "images.unsplash.com",
    "cdn.pixabay.com",
    "i.imgur.com",
    "upload.wikimedia.org",
    "picsum.photos",
    "placekitten.com",
    "flickr.com",
    "images.example.com",  # example placeholder
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def validate_picture_url(pic_url: str) -> str:
    """
    Validate that the provided image URL uses a trusted domain and an allowed scheme.
    
    Parameters
    ----------
    pic_url : str
        The image URL to validate.

    Returns
    -------
    str
        The original, fully resolved URL if it passes validation checks.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https or if the domain is not in the trusted list.
    """
    # Basic sanity check: non-empty string
    if not isinstance(pic_url, str) or not pic_url.strip():
        raise ValueError("pic_url must be a non-empty string")

    # Parse the URL
    parsed: ParseResult = urlparse(pic_url.strip())

    # Ensure scheme is allowed
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}'. Only HTTP/HTTPS are allowed.")

    # Extract the hostname; urlparse returns '' for URLs without a netloc
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL does not contain a valid host component")

    # Normalize the hostname (case-insensitive)
    hostname = hostname.lower()

    # Domain matching: support subdomains of trusted domains
    if not any(
        hostname == domain or hostname.endswith("." + domain)
        for domain in TRUSTED_DOMAINS
    ):
        raise ValueError(f"Domain '{hostname}' is not in the list of trusted providers")

    # Reconstruct the URL to ensure consistent formatting
    # This step also normalizes percent-encoding and removes default ports
    rebuilt_url = parsed.geturl()
    return rebuilt_url


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         url = validate_picture_url("https://i.imgur.com/abcd1234.png")
#         print(f"Valid URL: {url}")
#     except ValueError as e:
#         print(f"Validation error: {e}")