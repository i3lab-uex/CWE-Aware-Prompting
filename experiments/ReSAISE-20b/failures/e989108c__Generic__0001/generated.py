import re
from urllib.parse import urlparse, urlunparse

# List of approved image hosting domains (case‑insensitive)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "flickr.com",
    "static.flickr.com",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}


def get_image_link(link_image: str) -> str:
    """
    Validate and return a fully qualified image URL.

    Parameters
    ----------
    link_image : str
        The URL to validate and resolve.

    Returns
    -------
    str
        The validated, resolved image URL.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, is not absolute,
        or points to an untrusted domain.
    """
    if not isinstance(link_image, str):
        raise ValueError("link_image must be a string")

    # Parse the URL
    parsed = urlparse(link_image)

    # Must be an absolute URL with scheme and network location
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute and include scheme and host")

    # Scheme validation
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Domain validation (case‑insensitive)
    host = parsed.hostname.lower()
    if host not in _TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {host}")

    # Re‑assemble the URL to ensure consistent formatting
    cleaned = urlunparse(parsed._replace(fragment=""))
    return cleaned


# Example usage (commented out; remove comments to test):
# if __name__ == "__main__":
#     print(get_image_link("https://i.imgur.com/example.png"))