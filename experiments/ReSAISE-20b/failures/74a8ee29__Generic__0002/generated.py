import re
from urllib.parse import urlparse, urlunparse

# List of allowed image hosting domains (case‑insensitive)
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "pixabay.com",
    "cdn.pixabay.com",
    "flickr.com",
    "static.flickr.com",
    "media.tumblr.com",
    "cdn.discordapp.com",
    "images.unsplash.com",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def _normalize_url(url: str) -> str:
    """
    Normalise the URL for comparison:
      * lower‑case scheme and netloc
      * strip trailing slash from path (optional)
    """
    parsed = urlparse(url)
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/") or "/"
    return urlunparse((scheme, netloc, path, "", "", ""))


def check_image_link(image_link: str) -> str:
    """
    Validate that an image URL belongs to a trusted domain.

    Parameters
    ----------
    image_link : str
        The raw URL of the image to verify.

    Returns
    -------
    str
        The original URL if it passes validation.

    Raises
    ------
    ValueError
        If the scheme is unsupported or the domain is not in the trusted list.
    """
    if not isinstance(image_link, str):
        raise ValueError("image_link must be a string")

    parsed = urlparse(image_link)

    # Validate scheme
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate domain
    netloc = parsed.netloc.lower()
    if not any(netloc == d or netloc.endswith("." + d) for d in TRUSTED_DOMAINS):
        raise ValueError(f"Domain not trusted: {netloc}")

    # Optionally, you can normalise the URL before returning
    return image_link  # or _normalize_url(image_link)