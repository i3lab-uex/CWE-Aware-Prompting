import re
from urllib.parse import urlparse

import requests


# List of trusted image hosting domains (exact or subdomain matches)
_TRUSTED_DOMAINS = [
    "imgur.com",
    "i.imgur.com",
    "pbs.twimg.com",
    "upload.wikimedia.org",
    "cdn.discordapp.com",
    "media.discordapp.net",
]


def _is_trusted_domain(hostname: str) -> bool:
    """Return True if the hostname matches a trusted domain or its subdomain."""
    # Normalize hostname (remove trailing dot)
    hostname = hostname.rstrip(".").lower()
    for domain in _TRUSTED_DOMAINS:
        if hostname == domain or hostname.endswith("." + domain):
            return True
    return False


def check_image_link(image_link: str) -> str:
    """
    Resolve an image URL and return the final location if it points to a trusted
    domain. Raises ValueError for untrusted domains or unsupported schemes.

    Parameters:
        image_link (str): The URL of the image to validate and resolve.

    Returns:
        str: The resolved final URL that points to a trusted image host.

    Raises:
        ValueError: If the URL scheme is not http/https or if the host is not trusted.
        requests.RequestException: If the HTTP request fails for any reason.
    """
    # Parse the URL
    parsed = urlparse(image_link)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    if not _is_trusted_domain(parsed.hostname or ""):
        raise ValueError(f"Untrusted host: {parsed.hostname}")

    # Perform a HEAD request to follow redirects without downloading the whole image.
    # Disable any proxy configuration that might be set in the environment to avoid
    # accidental proxying (CWE-441 concern).
    session = requests.Session()
    try:
        response = session.head(
            image_link,
            allow_redirects=True,
            timeout=10,          # reasonable timeout
            headers={"User-Agent": "ImageValidator/1.0"},
            proxies={},          # explicitly disable proxies
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        # Propagate HTTP errors (e.g., 404, timeout) to the caller
        raise exc

    final_url = response.url

    # Verify that the final URL still points to a trusted domain
    parsed_final = urlparse(final_url)
    if not _is_trusted_domain(parsed_final.hostname or ""):
        raise ValueError(f"Redirected to untrusted host: {parsed_final.hostname}")

    return final_url