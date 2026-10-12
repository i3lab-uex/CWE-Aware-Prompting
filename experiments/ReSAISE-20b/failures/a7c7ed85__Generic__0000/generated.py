import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (add or modify as needed)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "cdn.example.com",
    "images.unsplash.com",
    "pics.flickr.com",
    # add more domains here
}

# Regular expression to match a domain or any of its sub‑domains
_DOMAIN_RE = re.compile(r"^(?:(?:[a-z0-9](?:[a-z0-9\-]{0,61}[a-z0-9])?\.)*)(?P<domain>[a-z0-9\-]+\.[a-z]{2,})$", re.IGNORECASE)


def _extract_base_domain(host: str) -> str | None:
    """
    Return the base domain (e.g. 'example.com') from a host,
    or None if it cannot be parsed.
    """
    match = _DOMAIN_RE.match(host)
    return match.group("domain") if match else None


def validate_image_url(img_url: str) -> str:
    """
    Validate that *img_url* points to a trusted image hosting provider.

    Parameters
    ----------
    img_url : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it is considered valid and trusted.

    Raises
    ------
    ValueError
        If the URL scheme is not ``http`` or ``https``, or if its host is not
        in the trusted domain list.
    """
    # Parse URL components
    parsed = urlparse(img_url)

    # Check scheme
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Resolve host to base domain
    host = parsed.hostname or ""
    base_domain = _extract_base_domain(host)
    if not base_domain:
        raise ValueError(f"Could not parse host from URL: {img_url!r}")

    # Validate against trusted list
    if base_domain.lower() not in _TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted host: {base_domain!r}")

    # Rebuild URL to ensure it's normalized (e.g., no default port)
    cleaned = parsed._replace(netloc=parsed.hostname or "")
    return urlunparse(cleaned)