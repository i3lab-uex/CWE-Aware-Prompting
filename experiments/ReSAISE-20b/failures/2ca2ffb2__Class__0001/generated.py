import re
from urllib.parse import urlparse

# List of domains that are considered trustworthy for image hosting.
TRUSTED_DOMAINS = {
    "imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "i.redd.it",
    "flickr.com",
}

# Regular expression to validate the scheme (http or https).
SCHEME_REGEX = re.compile(r"^(https?)$", re.IGNORECASE)


def fetch_image_url(url: str) -> str:
    """
    Resolve an image URL and ensure that it belongs to a trusted domain.

    Parameters
    ----------
    url : str
        The URL of the image to validate.

    Returns
    -------
    str
        The original URL if it is considered safe and trusted.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https or if the hostname does not belong to a trusted domain.
    """
    # Parse the URL
    parsed = urlparse(url)

    # Validate scheme
    if not SCHEME_REGEX.match(parsed.scheme):
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}'. Only HTTP and HTTPS are allowed.")

    # Ensure the hostname is present
    if not parsed.hostname:
        raise ValueError("URL does not contain a valid hostname.")

    # Normalize the domain to lowercase for comparison
    host = parsed.hostname.lower()

    # Check if hostname ends with one of the trusted domains.
    # This allows subdomains (e.g., i.imgur.com) to be accepted.
    if not any(host == domain or host.endswith("." + domain) for domain in TRUSTED_DOMAINS):
        raise ValueError(f"Hostname '{host}' is not trusted for image hosting.")

    # At this point the URL is considered safe; return it unchanged.
    return url