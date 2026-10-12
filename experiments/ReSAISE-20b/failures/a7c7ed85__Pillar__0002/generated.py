import urllib.parse

# List of trusted image hosting domains.
TRUSTED_DOMAINS = {
    "images.unsplash.com",
    "picsum.photos",
    "cdn.pixabay.com",
    "flickr.com",
    "images.unsplash.com",
    "i.imgur.com",
    "cdn.pexels.com",
}

# Allowed URL schemes.
ALLOWED_SCHEMES = {"http", "https"}


def validate_image_url(img_url: str) -> str:
    """
    Validate that an image URL belongs to a trusted domain and uses
    an allowed scheme. Returns the normalized absolute URL.

    Args:
        img_url: The image URL to validate.

    Raises:
        ValueError: If the domain is not trusted or scheme unsupported.
        TypeError: If `img_url` is not a string.

    Returns:
        str: The fully resolved, validated URL.
    """
    if not isinstance(img_url, str):
        raise TypeError("img_url must be a string")

    # Parse the URL components.
    parsed = urllib.parse.urlparse(img_url)

    # Ensure scheme is present and supported.
    if not parsed.scheme or parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(
            f"Unsupported URL scheme: {parsed.scheme!r}. "
            f"Allowed schemes are: {', '.join(ALLOWED_SCHEMES)}"
        )

    # Resolve relative URLs against a base if needed.
    if not parsed.netloc:
        raise ValueError("URL must contain a domain (netloc)")

    # Extract host and compare against trusted list.
    hostname = parsed.hostname.lower()
    if hostname not in TRUSTED_DOMAINS:
        raise ValueError(
            f"Domain {hostname!r} is not in the list of trusted providers"
        )

    # Reconstruct a normalized URL (remove fragments, query params if desired).
    normalized = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return normalized