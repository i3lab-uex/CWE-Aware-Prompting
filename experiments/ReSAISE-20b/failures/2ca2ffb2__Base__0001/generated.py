import re
from urllib.parse import urlparse, urlunparse

import requests


# A simple whitelist of trusted image hosting domains.
_TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "farm4.staticflickr.com",
    "images.pexels.com",
}


def _is_trusted_domain(domain: str) -> bool:
    """Check if the domain (or a sub‑domain of it) is in the whitelist."""
    # Strip port if present
    domain = domain.split(":")[0].lower()
    # A domain is trusted if it matches exactly or ends with `.<trusted>`
    for trusted in _TRUSTED_DOMAINS:
        if domain == trusted or domain.endswith("." + trusted):
            return True
    return False


def _validate_scheme(parsed: "ParseResult") -> None:
    """Ensure the URL scheme is HTTP or HTTPS."""
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")


def _validate_redirects(session: requests.Session, url: str) -> str:
    """
    Perform a HEAD request to the URL and follow redirects.
    Each redirect target must belong to the trusted domain list.
    """
    try:
        resp = session.head(url, allow_redirects=True, timeout=10)
    except requests.RequestException as exc:
        raise ValueError(f"Unable to fetch URL: {exc}") from exc

    # Validate the final location
    final_url = resp.url
    parsed_final = urlparse(final_url)
    _validate_scheme(parsed_final)

    if not _is_trusted_domain(parsed_final.netloc):
        raise ValueError(f"Redirected to untrusted domain: {parsed_final.netloc!r}")

    return final_url


def fetch_image_url(url: str) -> str:
    """
    Resolve an image URL, ensuring it points to a trusted domain.

    Parameters
    ----------
    url : str
        The original image URL supplied by the caller.

    Returns
    -------
    str
        The verified, possibly redirected, image URL.

    Raises
    ------
    ValueError
        If the URL scheme is unsupported, the domain is not trusted,
        or a redirect leads to an untrusted domain.
    """
    if not isinstance(url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(url)
    _validate_scheme(parsed)

    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Domain not trusted: {parsed.netloc!r}")

    # Use a session to follow redirects safely
    with requests.Session() as sess:
        final_url = _validate_redirects(sess, url)

    # Optionally, you could perform a quick GET to ensure the content type is an image.
    try:
        head_resp = sess.head(final_url, allow_redirects=False, timeout=10)
    except requests.RequestException as exc:
        raise ValueError(f"Failed to fetch final URL: {exc}") from exc

    content_type = head_resp.headers.get("Content-Type", "")
    if not re.match(r"image/(jpeg|png|gif|webp|bmp)", content_type, re.I):
        raise ValueError(f"Content at final URL is not an image: {content_type!r}")

    return final_url