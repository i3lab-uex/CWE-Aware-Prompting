import re
from urllib.parse import urlparse

# List of approved image hosting domains.
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "imgur.com",
    "cdn.discordapp.com",
    "media.discordapp.net",
    "images.unsplash.com",
    "flickr.com",
    "static.flickr.com",
    "picsum.photos",
}

# Allowed URL schemes.
ALLOWED_SCHEMES = {"http", "https"}


def _normalize_netloc(netloc: str) -> str:
    """
    Normalise the netloc component by lower‑casing and stripping any
    port number.
    """
    host, _, _ = netloc.partition(":")
    return host.lower()


def _is_trusted_domain(host: str) -> bool:
    """
    Return True if the host ends with one of the trusted domains.
    This allows subdomains to be accepted (e.g. a.imgur.com).
    """
    host = _normalize_netloc(host)
    return any(host == domain or host.endswith("." + domain) for domain in TRUSTED_DOMAINS)


def check_image_link(image_link: str) -> str:
    """
    Verify that *image_link* points to a trusted image hosting domain.

    Parameters
    ----------
    image_link : str
        The URL of the image to validate.

    Returns
    -------
    str
        The original *image_link* if it is trusted.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https or if the host does not belong to a trusted domain.
    """
    if not isinstance(image_link, str):
        raise ValueError("image_link must be a string")

    parsed = urlparse(image_link)

    # Check scheme
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unrecognized URL scheme: {parsed.scheme!r}")

    # Check host
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (host)")

    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.netloc!r}")

    # Optionally, validate that the path ends with a common image extension.
    # This is not strictly required but helps catch non‑image URLs.
    if not re.search(r"\.(png|jpe?g|gif|webp)(\?.*)?$", parsed.path, re.IGNORECASE):
        raise ValueError("URL does not point to a common image file")

    return image_link