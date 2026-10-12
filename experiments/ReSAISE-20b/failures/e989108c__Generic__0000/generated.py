import re
from urllib.parse import urlparse, urlunparse

# List of approved image hosting domains (case‑insensitive)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "postimages.org",
    "picsum.photos",
    "flickr.com",
    "upload.wikimedia.org",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}

# Optional: common image file extensions for a stricter check
_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}


def _is_trusted_domain(netloc: str) -> bool:
    """Return True if the netloc is in the trusted domain list."""
    # Normalize to lowercase and strip port if present
    host = netloc.split(":")[0].lower()
    return host in _TRUSTED_DOMAINS


def _has_valid_image_extension(path: str) -> bool:
    """Check if the URL path ends with a known image extension."""
    return any(path.lower().endswith(ext) for ext in _IMAGE_EXTENSIONS)


def get_image_link(link_image: str) -> str:
    """
    Validate an image URL and return the resolved, canonical form.

    Parameters
    ----------
    link_image : str
        The image URL to validate and resolve.

    Returns
    -------
    str
        The validated, fully qualified image URL.

    Raises
    ------
    ValueError
        If the scheme is unsupported, the domain is untrusted,
        or the path does not look like an image file.
    """
    if not isinstance(link_image, str):
        raise ValueError("link_image must be a string")

    parsed = urlparse(link_image)

    # 1. Scheme check
    if parsed.scheme not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # 2. Domain check
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.netloc!r}")

    # 3. Path / extension check (optional but recommended)
    if not parsed.path or not _has_valid_image_extension(parsed.path):
        raise ValueError(f"URL does not point to a recognized image file: {link_image!r}")

    # 4. Reconstruct the URL to ensure it is canonical
    #    (e.g., remove fragments, normalize slashes)
    normalized = urlunparse((
        parsed.scheme,
        parsed.netloc.lower(),
        re.sub(r"/+", "/", parsed.path),  # collapse multiple slashes
        "",  # params
        parsed.query,
        ""   # fragment removed for safety
    ))

    return normalized