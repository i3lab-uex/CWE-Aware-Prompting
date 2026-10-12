import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (case‑insensitive)
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.mytrusteddomain.org",
    "photos.safe-site.net",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def _normalize_domain(domain: str) -> str:
    """
    Normalise a domain by stripping leading/trailing whitespace and
    converting to lowercase.
    """
    return domain.strip().lower()


def _is_trusted(domain: str) -> bool:
    """
    Return True if the domain is in the TRUSTED_DOMAINS set.
    Handles sub‑domains that are explicitly listed.
    """
    domain = _normalize_domain(domain)
    return domain in TRUSTED_DOMAINS


def get_image_link(link_image: str) -> str:
    """
    Validate that *link_image* is a URL pointing to an image hosted on one
    of the trusted domains and that it uses http or https.

    Parameters
    ----------
    link_image : str
        The image URL to check and resolve.

    Returns
    -------
    str
        The validated, fully‑qualified URL.

    Raises
    ------
    ValueError
        If the URL has an unsupported scheme or points to an untrusted domain.
    """
    if not isinstance(link_image, str):
        raise ValueError("link_image must be a string")

    # Parse the URL
    parsed = urlparse(link_image)

    # Scheme check (must be http or https)
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Domain check
    domain = parsed.hostname
    if not domain:
        raise ValueError("URL must contain a hostname")

    if not _is_trusted(domain):
        raise ValueError(f"Untrusted domain: {domain}")

    # Re‑build the URL to ensure it is normalized
    cleaned = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))

    return cleaned