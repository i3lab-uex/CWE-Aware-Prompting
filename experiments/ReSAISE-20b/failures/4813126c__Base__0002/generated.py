import urllib.parse

# Trusted image hosting domains (add or remove as needed)
_TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "flickr.com",
    "githubusercontent.com",
    "res.cloudinary.com",
}


def verify_image_url(img_url: str) -> str:
    """
    Verify that an image URL belongs to a trusted domain and has a safe scheme.

    Parameters
    ----------
    img_url : str
        The URL of the image to validate.

    Returns
    -------
    str
        The original URL if it passes validation.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP/HTTPS or the domain is not in the trusted list.
    """
    # Parse the URL
    parsed = urllib.parse.urlparse(img_url)

    # Ensure scheme is http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Normalize hostname (strip port if present)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Check against trusted domains
    if host.lower() not in _TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {host!r}")

    # Reconstruct the URL to ensure consistent formatting
    safe_url = urllib.parse.urlunparse(parsed)
    return safe_url