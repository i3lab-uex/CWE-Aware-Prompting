import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains.
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "pbs.twimg.com",
    "media.discordapp.net",
    "cdn.discordapp.com",
    "i.redd.it",
}

# Allowed schemes.
ALLOWED_SCHEMES = {"http", "https"}


def _is_trusted_domain(netloc: str) -> bool:
    """
    Check if the provided netloc (hostname) belongs to a trusted domain.
    Subdomains are accepted only if they exactly match an entry in TRUSTED_DOMAINS.
    """
    # Remove port number if present
    host = netloc.split(":")[0].lower()
    return host in TRUSTED_DOMAINS


def get_image_link(link_image: str) -> str:
    """
    Validate and return a fully-qualified image URL.

    Parameters
    ----------
    link_image : str
        The image URL to validate and resolve.

    Returns
    -------
    str
        The validated, absolute URL.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, is not absolute,
        or points to an untrusted domain.
    """
    if not isinstance(link_image, str):
        raise ValueError("link_image must be a string")

    # Parse the URL
    parsed = urlparse(link_image)

    # Must be absolute (scheme + netloc)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute and include scheme and host")

    # Scheme validation
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Domain validation
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.netloc}")

    # Reconstruct the URL to ensure it is in a canonical form
    normalized = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))

    return normalized