import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (add or remove as needed)
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "picsum.photos",
    "cdn.pixabay.com",
    "flickr.com",
    "storage.googleapis.com",
}

# Regular expression to match a valid URL scheme
_SCHEME_RE = re.compile(r"^(http|https)://", re.IGNORECASE)


def fetch_image_url(img_url: str) -> str:
    """
    Validate that *img_url* points to a trusted image hosting domain and
    return the normalized absolute URL.

    Parameters
    ----------
    img_url : str
        The image URL to validate and resolve.

    Returns
    -------
    str
        The validated, absolute URL ready for use.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP/HTTPS or the domain is not trusted.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    # Ensure the URL has a scheme
    if not _SCHEME_RE.match(img_url):
        raise ValueError("URL must start with http:// or https://")

    parsed = urlparse(img_url)

    # Verify scheme
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalize the netloc to lowercase for comparison
    domain = parsed.hostname.lower() if parsed.hostname else ""
    if domain not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted image host: {domain}")

    # Rebuild the URL to ensure it is fully qualified
    cleaned = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            "",  # params
            parsed.query or "",
            parsed.fragment or "",
        )
    )

    return cleaned