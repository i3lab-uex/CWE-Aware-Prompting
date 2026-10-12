import re
from urllib.parse import urlparse, ParseResult

# List of domains that are considered trustworthy for image hosting
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "images.unsplash.com",
    "picsum.photos",
    "flickr.com",
    "cdn.pixabay.com",
    "upload.wikimedia.org",
}

# Regular expression to validate URLs (basic check)
URL_REGEX = re.compile(
    r"^(?P<scheme>https?)://"
    r"(?P<host>[^/]+)"
    r"(?:/(?P<path>.*))?$",
    re.IGNORECASE,
)

def check_image_link(image_link: str) -> str:
    """
    Validate that the supplied image URL belongs to a trusted domain and
    return the normalized URL.

    Parameters:
        image_link (str): The raw image URL to validate.

    Returns:
        str: The validated and normalized image URL.

    Raises:
        ValueError: If the URL is malformed, has an unsupported scheme,
                    or its host is not in TRUSTED_DOMAINS.
    """
    if not isinstance(image_link, str):
        raise ValueError("image_link must be a string")

    # Parse the URL
    match = URL_REGEX.match(image_link.strip())
    if not match:
        raise ValueError(f"Malformed URL: {image_link!r}")

    scheme = match.group("scheme").lower()
    host = match.group("host").lower()

    # Ensure scheme is HTTP or HTTPS
    if scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {scheme!r}")

    # Strip port if present
    host = host.split(":")[0]

    # Validate domain against the trusted list
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {host!r}")

    # Reconstruct a canonical URL (no fragment, keep path/query)
    parsed = urlparse(image_link)
    normalized: ParseResult = parsed._replace(fragment="")  # remove fragment
    return normalized.geturl()