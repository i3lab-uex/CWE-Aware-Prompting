import re
from urllib.parse import urlparse

# A small set of domains that are considered trusted for image hosting.
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "static.wikia.nocookie.net",  # example of a CDN
}

# Regular expression for matching a valid HTTP or HTTPS scheme.
SCHEME_RE = re.compile(r"^(http|https)://", re.IGNORECASE)


def check_image_link(image_link: str) -> str:
    """
    Validate that an image URL points to a trusted domain and uses a safe scheme.

    Parameters
    ----------
    image_link : str
        The URL of the image to resolve.

    Returns
    -------
    str
        The original URL if it is considered safe and trusted.

    Raises
    ------
    ValueError
        If the URL's scheme is not http/https or if its host is not in the trusted list.
    """
    # Basic validation of scheme
    if not SCHEME_RE.match(image_link):
        raise ValueError("URL must start with http:// or https://")

    # Parse the URL
    parsed = urlparse(image_link)

    # Ensure we have a hostname
    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    # Normalize the hostname to lower case for comparison
    host = parsed.hostname.lower()

    # Verify that the domain is trusted.  We allow subdomains of
    # the trusted domains (e.g., i.imgur.com for imgur.com).
    if not any(host == domain or host.endswith("." + domain) for domain in TRUSTED_DOMAINS):
        raise ValueError(f"Domain '{host}' is not trusted")

    # The URL passes all checks; return it unchanged.
    return image_link