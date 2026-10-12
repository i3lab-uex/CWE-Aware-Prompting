import re
from urllib.parse import urlparse, ParseResult
import requests

# List of trusted image hosting domains (add or remove as needed)
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "flickr.com",
    "imgur.com",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def _is_trusted_domain(domain: str) -> bool:
    """
    Check if the provided domain (or any of its parent domains)
    matches one of the trusted domains.
    """
    # Normalize subdomains: e.g., foo.imgur.com should match imgur.com
    parts = domain.lower().split(".")
    for i in range(len(parts)):
        candidate = ".".join(parts[i:])
        if candidate in TRUSTED_DOMAINS:
            return True
    return False


def get_image_link(link_image: str) -> str:
    """
    Validate and resolve an image URL.

    Parameters
    ----------
    link_image : str
        The URL to validate and resolve.

    Returns
    -------
    str
        The resolved, fully-qualified image URL if the domain is trusted.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, or if its domain is not trusted.
    """
    # Parse the URL
    parsed: ParseResult = urlparse(link_image)

    if not parsed.scheme or parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(
            f"Unsupported URL scheme '{parsed.scheme}'. Only HTTP/HTTPS are allowed."
        )

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain).")

    # Validate domain
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not trusted.")

    # Optionally follow redirects to get the final URL
    try:
        resp = requests.get(
            link_image,
            allow_redirects=True,
            timeout=10,  # seconds
            headers={"User-Agent": "ImageValidator/1.0"},
        )
    except requests.RequestException as exc:
        raise ValueError(f"Failed to retrieve URL: {exc}") from exc

    # Ensure the final location is still trusted
    final_url = resp.url
    final_parsed = urlparse(final_url)
    if not _is_trusted_domain(final_parsed.netloc):
        raise ValueError(
            f"Redirected to untrusted domain '{final_parsed.netloc}'."
        )

    return final_url