import re
from urllib.parse import urlparse

import requests
from requests.exceptions import RequestException


# ------------------------------------------------------------------
# Trusted image hosting domains (add more as needed)
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "picsum.photos",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "flickr.com",
    "static.flickr.com",
    "i.redd.it",
}

# Regular expression for a valid HTTP/HTTPS URL
URL_REGEX = re.compile(
    r"^(?P<scheme>https?)://(?P<host>[^/]+)(?P<path>/.*)?$",
    re.IGNORECASE,
)


def _is_trusted(host: str) -> bool:
    """
    Return True if the host is in TRUSTED_DOMAINS or ends with one of them.
    """
    host = host.lower()
    return any(host == d or host.endswith("." + d) for d in TRUSTED_DOMAINS)


def check_image_link(image_link: str) -> str:
    """
    Validate that *image_link* points to a trusted image hosting domain and
    return the final URL after following redirects (if any).

    Parameters
    ----------
    image_link : str
        The URL of the image to resolve.

    Returns
    -------
    str
        The verified final image URL.

    Raises
    ------
    ValueError
        If the scheme is not HTTP/HTTPS or if the domain (initial or final)
        is not trusted.
    RuntimeError
        If an HTTP error occurs while resolving the URL.
    """
    # Basic syntax validation
    match = URL_REGEX.match(image_link)
    if not match:
        raise ValueError(f"Invalid URL format: {image_link}")

    scheme = match.group("scheme").lower()
    host = match.group("host")

    if not _is_trusted(host):
        raise ValueError(f"Untrusted host: {host}")

    # Perform a HEAD request to follow redirects without downloading the body.
    try:
        session = requests.Session()
        # Disable SSL verification only if you trust the environment; keep it enabled by default.
        resp = session.head(
            image_link,
            allow_redirects=True,
            timeout=10,  # seconds
        )
    except RequestException as exc:
        raise RuntimeError(f"Failed to resolve image URL: {exc}") from exc

    final_url = resp.url
    parsed_final = urlparse(final_url)

    # Ensure the final host is also trusted
    if not _is_trusted(parsed_final.hostname or ""):
        raise ValueError(f"Redirected to untrusted host: {parsed_final.hostname}")

    return final_url