import re
from urllib.parse import urlparse, ParseResult

# --------------------------------------------------------------------------- #
# Trusted image hosting domains (add or remove as needed)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "cdn.discordapp.com",
    "images.unsplash.com",
    "picsum.photos",
    "flickr.com",
}

# --------------------------------------------------------------------------- #
def _extract_domain(parsed: ParseResult) -> str:
    """
    Return the domain part of a parsed URL.
    Handles IPv4/IPv6 addresses and optional port numbers.
    """
    host = parsed.hostname or ""
    # Normalise to lowercase for comparison
    return host.lower()

# --------------------------------------------------------------------------- #
def check_image_link(image_link: str) -> str:
    """
    Validate that an image URL belongs to a trusted domain.

    Parameters
    ----------
    image_link : str
        The original URL of the image to validate.

    Returns
    -------
    str
        The verified image URL (unchanged from input).

    Raises
    ------
    ValueError
        If the scheme is not HTTP(S) or if the domain is not trusted.
    """
    # Basic URL parsing
    parsed = urlparse(image_link)

    if not parsed.scheme or parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unrecognised URL scheme: {parsed.scheme!r}")

    domain = _extract_domain(parsed)

    if domain not in _TRUSTED_DOMAINS:
        raise ValueError(f"Domain {domain!r} is not trusted")

    # The URL itself is considered safe; no further resolution to avoid
    # redirect-based domain spoofing or resource exhaustion.
    return image_link

# --------------------------------------------------------------------------- #
# Example usage (commented out for production code)
if __name__ == "__main__":
    test_urls = [
        "https://i.imgur.com/abc123.jpg",
        "http://cdn.discordapp.com/embed/avatars/0.png",
        "https://example.com/not-trusted.jpg",
    ]

    for url in test_urls:
        try:
            verified = check_image_link(url)
            print(f"✅ Valid: {verified}")
        except ValueError as exc:
            print(f"❌ Invalid: {url} -> {exc}")