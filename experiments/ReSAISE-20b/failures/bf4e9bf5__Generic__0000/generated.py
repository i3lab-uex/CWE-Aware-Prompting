import re
from urllib.parse import urlparse

import requests


# List of domains that are considered trusted image hosts.
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trusted.com",
    "static.safe-host.org",
}


def _is_trusted_domain(domain: str) -> bool:
    """
    Check if a domain or its parent domains are in the trusted list.
    e.g. sub.images.example.com is allowed because images.example.com is trusted.
    """
    domain = domain.lower()
    for trusted in TRUSTED_DOMAINS:
        if domain == trusted or domain.endswith("." + trusted):
            return True
    return False


def resolve_image_url(image_url: str) -> str:
    """
    Resolve an image URL by following redirects and ensuring the final domain
    belongs to a trusted host.

    Parameters
    ----------
    image_url : str
        The URL of the image to resolve.

    Returns
    -------
    str
        The final resolved URL if it belongs to a trusted domain.

    Raises
    ------
    ValueError
        If the input is not a valid URL, if the final domain is not trusted,
        or if any network error occurs.
    """
    if not isinstance(image_url, str) or not image_url.strip():
        raise ValueError("image_url must be a non‑empty string")

    # Basic URL validation
    parsed = urlparse(image_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {image_url!r}")

    # Perform the request with a short timeout and allow redirects
    try:
        session = requests.Session()
        # Limit the number of redirects to avoid infinite loops
        response = session.get(
            image_url,
            allow_redirects=True,
            timeout=10,  # seconds
        )
    except requests.exceptions.RequestException as exc:
        raise ValueError(f"Network error while resolving URL: {exc}") from exc

    final_url = response.url
    final_domain = urlparse(final_url).netloc.split(":")[0]  # ignore port

    if not _is_trusted_domain(final_domain):
        raise ValueError(
            f"Untrusted domain '{final_domain}' in resolved URL: {final_url}"
        )

    return final_url