import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (case‑insensitive)
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "pbs.twimg.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "flickr.com",
    "static.flickr.com",
    "images.pexels.com",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def _is_trusted_domain(host: str) -> bool:
    """Check if the hostname belongs to a trusted domain."""
    host = host.lower()
    # Handle subdomains: accept if any suffix matches a trusted domain
    return any(host == td or host.endswith("." + td) for td in TRUSTED_DOMAINS)


def get_image_link(link_image: str) -> str:
    """
    Validate and resolve an image URL.

    Parameters
    ----------
    link_image : str
        The image URL to validate and resolve.

    Returns
    -------
    str
        A fully resolved, trusted image URL.

    Raises
    ------
    ValueError
        If the URL scheme is unsupported, the domain is untrusted,
        or the URL is malformed.
    """
    if not isinstance(link_image, str):
        raise ValueError("link_image must be a string")

    parsed = urlparse(link_image)

    # Ensure scheme is present and allowed
    if not parsed.scheme or parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Validate host
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (host)")

    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.netloc!r}")

    # Rebuild the URL to ensure it is normalized
    cleaned = parsed._replace(
        path=re.sub(r"/+", "/", parsed.path),
        params="",
        query="",
        fragment="",
    )
    return urlunparse(cleaned)


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    test_urls = [
        "https://i.imgur.com/abcd1234.png",
        "http://images.unsplash.com/photo-1234567890?ixid=Mnw...",
        "https://evil.com/attack.png",
    ]

    for url in test_urls:
        try:
            print(f"Validated: {get_image_link(url)}")
        except ValueError as e:
            print(f"Rejected: {url} -> {e}")