import re
from urllib.parse import urlparse

import requests


# List of domains that are considered trusted image hosts.
_TRUSTED_DOMAINS = {
    "i.imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "res.cloudinary.com",
    "storage.googleapis.com",
}

# Allowed URL schemes.
_ALLOWED_SCHEMES = {"http", "https"}


def _is_trusted_domain(domain: str) -> bool:
    """
    Check if the given domain is in the set of trusted domains.
    The comparison is case‑insensitive and ignores leading “www.”.
    """
    domain = domain.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    return domain in _TRUSTED_DOMAINS


def check_image_link(image_link: str) -> str:
    """
    Resolve an image URL and verify that the final destination
    belongs to a trusted domain.

    Parameters
    ----------
    image_link : str
        The URL of the image to validate.

    Returns
    -------
    str
        The final resolved URL after following redirects.

    Raises
    ------
    ValueError
        If the scheme is not http/https, or if the final URL's domain
        is not in the trusted list.
    """
    # Basic validation of the input URL structure.
    parsed = urlparse(image_link)
    if not parsed.scheme or parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Perform a HEAD request to follow redirects without downloading the entire image.
    session = requests.Session()
    try:
        resp = session.head(
            image_link,
            allow_redirects=True,
            timeout=10,  # seconds
            headers={"User-Agent": "ImageLinkChecker/1.0"},
        )
    except requests.RequestException as exc:
        raise ValueError(f"Could not resolve URL {image_link!r}: {exc}") from exc

    # The final URL after redirects.
    final_url = resp.url
    final_parsed = urlparse(final_url)

    # Ensure the final domain is trusted.
    if not _is_trusted_domain(final_parsed.netloc):
        raise ValueError(
            f"Domain {final_parsed.netloc!r} is not trusted. "
            f"Final URL: {final_url}"
        )

    # Optional: ensure the final URL points to an image by checking extension or MIME type.
    if not re.search(r"\.(png|jpg|jpeg|gif|webp)$", final_parsed.path, re.IGNORECASE):
        # If the path does not contain a common image extension,
        # perform an extra GET to check the Content‑Type header.
        try:
            resp = session.get(final_url, stream=True, timeout=10)
            content_type = resp.headers.get("Content-Type", "")
        except requests.RequestException:
            raise ValueError(f"Unable to fetch image headers from {final_url}")
        if not content_type.lower().startswith("image/"):
            raise ValueError(
                f"URL does not point to an image. Content-Type: {content_type!r}"
            )

    return final_url