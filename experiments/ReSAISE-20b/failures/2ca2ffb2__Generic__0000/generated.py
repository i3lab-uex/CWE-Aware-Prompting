import urllib.parse

# List of trusted image hosting domains (case‑insensitive)
_TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "placehold.it",
    "picsum.photos",
}

def fetch_image_url(url: str) -> str:
    """
    Validate an image URL against a whitelist of trusted domains.

    Parameters
    ----------
    url : str
        The image URL to validate and return.

    Returns
    -------
    str
        The original URL if it passes validation.

    Raises
    ------
    ValueError
        If the scheme is not HTTP/HTTPS or if the domain is not in the trusted list.
    """
    if not isinstance(url, str):
        raise ValueError("URL must be a string")

    parsed = urllib.parse.urlparse(url)

    # Scheme check
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Domain check (case‑insensitive)
    netloc = parsed.netloc.lower()
    if not any(netloc == domain or netloc.endswith("." + domain) for domain in _TRUSTED_DOMAINS):
        raise ValueError(f"Domain {netloc!r} is not trusted")

    return url