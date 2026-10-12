import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (exact matches or sub‑domains)
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "flickr.com",
}

# Regular expression to validate the domain part (allow subdomains)
DOMAIN_REGEX = re.compile(r"^(?:[a-zA-Z0-9-]+\.)*([a-zA-Z0-9-]+\.[a-zA-Z]{2,})$")


def _extract_registered_domain(host: str) -> str | None:
    """
    Extract the registered domain from a hostname.
    For example, 'sub.example.com' -> 'example.com'.
    Returns None if the host does not contain a valid domain.
    """
    match = DOMAIN_REGEX.match(host)
    if match:
        return match.group(1).lower()
    return None


def get_image_link(link_image: str) -> str:
    """
    Validate that an image URL points to a trusted provider and return the
    fully resolved absolute URL.

    Parameters
    ----------
    link_image : str
        The image URL to validate and resolve.

    Returns
    -------
    str
        The validated absolute URL.

    Raises
    ------
    ValueError
        If the URL has an unsupported scheme, is not absolute,
        or points to an untrusted domain.
    """
    if not isinstance(link_image, str):
        raise ValueError("link_image must be a string")

    # Parse the URL
    parsed = urlparse(link_image)

    # Validate scheme
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Validate that the URL is absolute
    if not parsed.netloc:
        raise ValueError("URL must be absolute (include scheme and host)")

    # Normalize the netloc to lower case
    host = parsed.netloc.lower()

    # Verify that the host is within the trusted domains list
    if not any(host == domain or host.endswith("." + domain) for domain in TRUSTED_DOMAINS):
        raise ValueError(f"Untrusted host: {host!r}")

    # Reconstruct the absolute URL (in case the input was relative)
    normalized = urlunparse(parsed._replace(path=parsed.path or "/", params="", query="", fragment=""))

    return normalized