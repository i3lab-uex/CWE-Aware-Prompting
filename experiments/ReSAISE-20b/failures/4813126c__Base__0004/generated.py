import re
from urllib.parse import urlparse

# List of domains that are considered trustworthy for image hosting.
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "static.tumblr.com",
    "pbs.twimg.com",
    # add more domains as needed
}

# Regular expression to validate URL scheme (http or https)
_SCHEME_RE = re.compile(r"^(https?)://", re.IGNORECASE)


def verify_image_url(img_url: str) -> str:
    """
    Verify that an image URL points to a trusted domain and uses http or https.

    Parameters
    ----------
    img_url : str
        The URL of the image to validate.

    Returns
    -------
    str
        The validated, normalized URL.

    Raises
    ------
    ValueError
        If the URL is malformed, has an unrecognized scheme, or does not belong to a trusted domain.
    """
    if not isinstance(img_url, str):
        raise ValueError("Image URL must be a string")

    # Quick check for scheme
    if not _SCHEME_RE.match(img_url):
        raise ValueError("Unrecognized URL scheme; only http and https are allowed")

    # Parse the URL
    parsed = urlparse(img_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL")

    # Normalize the domain to lowercase for comparison
    host = parsed.netloc.lower()

    # Remove port if present (e.g., example.com:8080)
    host = host.split(":")[0]

    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not trusted")

    # Return the original URL (or you could reassemble it if normalization is desired)
    return img_url