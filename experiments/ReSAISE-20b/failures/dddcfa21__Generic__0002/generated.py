import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (case‑insensitive)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "static.wikia.nocookie.net",
    "cdn.jsdelivr.net",
}

# Optional: allow only common image extensions
_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}


def check_image_url(img_address: str) -> str:
    """
    Validate that an image URL points to a trusted host and uses http/https.

    Parameters
    ----------
    img_address : str
        The image URL to validate.

    Returns
    -------
    str
        The fully resolved, validated URL.

    Raises
    ------
    ValueError
        If the scheme is not http/https or the host/domain is not trusted.
    """
    if not isinstance(img_address, str):
        raise ValueError("img_address must be a string")

    # Parse the URL
    parsed = urlparse(img_address)

    # Ensure scheme is http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Normalise the hostname (lowercase, strip port)
    host = parsed.hostname.lower() if parsed.hostname else ""
    if not host:
        raise ValueError("URL must contain a hostname")

    # Check against trusted domains
    if host not in _TRUSTED_DOMAINS:
        raise ValueError(f"Domain {host!r} is not trusted")

    # Optional: Ensure the path ends with a known image extension
    if parsed.path:
        _, ext = re.splitext(parsed.path)
        if ext.lower() not in _IMAGE_EXTENSIONS:
            raise ValueError(f"URL path does not end with a recognized image extension: {ext!r}")

    # Reconstruct the URL to ensure consistency
    cleaned = parsed._replace(path=parsed.path, params="", query="", fragment="")
    return urlunparse(cleaned)


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    test_urls = [
        "https://i.imgur.com/abcd1234.jpg",
        "http://cdn.pixabay.com/photo/2020/01/01/12/00/abcd-1234.png",
        "https://example.com/image.jpg",  # should raise
    ]

    for url in test_urls:
        try:
            print("Valid:", check_image_url(url))
        except ValueError as exc:
            print(f"Invalid: {url} -> {exc}")