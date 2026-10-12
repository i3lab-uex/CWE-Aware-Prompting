import re
from urllib.parse import urlparse

import requests


def check_image_link(image_link: str) -> str:
    """
    Validate that an image URL points to a trusted domain and return the final
    resolved URL after following redirects.

    Parameters
    ----------
    image_link : str
        The original image URL to validate and resolve.

    Returns
    -------
    str
        The final resolved URL after following redirects, if the domain is trusted.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https, or if the domain (after any redirects)
        does not belong to a trusted image hosting service.
    """
    # List of trusted domains (case‑insensitive)
    TRUSTED_DOMAINS = {
        "imgur.com",
        "i.imgur.com",
        "postimage.org",
        "flickr.com",
    }

    # Basic syntax check
    parsed = urlparse(image_link)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Resolve redirects safely
    try:
        resp = requests.head(
            image_link,
            allow_redirects=True,
            timeout=5,          # seconds
            headers={"User-Agent": "image-link-validator/1.0"},
        )
    except requests.RequestException as exc:
        raise ValueError(f"Unable to reach URL: {exc}") from exc

    final_url = resp.url
    final_parsed = urlparse(final_url)

    # Extract the domain part (netloc may include port)
    host = final_parsed.hostname
    if not host:
        raise ValueError("URL does not contain a valid hostname")

    # Normalize to lower case for comparison
    host_lower = host.lower()

    # Verify the domain is trusted
    if not any(host_lower == d or host_lower.endswith(f".{d}") for d in TRUSTED_DOMAINS):
        raise ValueError(f"Domain '{host}' is not trusted")

    return final_url