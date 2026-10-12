import re
from urllib.parse import urlparse, urlunparse, ParseResult

# --------------------------------------------------------------------------- #
# Trusted image hosting providers
# Add or remove domains as needed. Subdomains are also accepted.
_TRUSTED_DOMAINS = {
    "imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "picsum.photos",
    "flickr.com",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}

# --------------------------------------------------------------------------- #
def validate_image_source(img_src: str) -> str:
    """
    Validate that *img_src* points to an image hosted on a trusted provider.
    
    Parameters
    ----------
    img_src : str
        The image URL to validate.

    Returns
    -------
    str
        The normalized, absolute URL if it is trusted and uses an allowed scheme.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme or points to an untrusted domain.
    """
    if not isinstance(img_src, str):
        raise ValueError("img_src must be a string")

    # Parse the URL
    parsed = urlparse(img_src.strip())
    
    # Validate scheme
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate host
    hostname = parsed.hostname or ""
    hostname = hostname.lower()
    if not any(hostname == domain or hostname.endswith("." + domain)
               for domain in _TRUSTED_DOMAINS):
        raise ValueError(f"Untrusted host: {hostname}")

    # Reconstruct the URL to ensure consistent formatting
    normalized = ParseResult(
        scheme=parsed.scheme.lower(),
        netloc=hostname,
        path=re.sub(r"/+", "/", parsed.path),  # collapse multiple slashes
        params="",
        query=parsed.query,
        fragment=""
    )
    
    return urlunparse(normalized)

# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
if __name__ == "__main__":
    test_urls = [
        "https://i.imgur.com/abcd1234.png",
        "http://cdn.pixabay.com/photo/2020/01/01/12/34/56/sample.jpg",
        "https://malicious.com/image.png",
        "ftp://imgur.com/abcd1234.png",
    ]
    
    for url in test_urls:
        try:
            print(f"Valid: {validate_image_source(url)}")
        except ValueError as e:
            print(f"Invalid: {url} -> {e}")