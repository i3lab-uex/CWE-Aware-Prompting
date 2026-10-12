import re
from urllib.parse import urlparse, ParseResult

# List of approved image hosting domains (exact match or subdomain)
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "pbs.twimg.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
}

# Allowed schemes
ALLOWED_SCHEMES = {"http", "https"}

def _is_trusted_domain(host: str) -> bool:
    """
    Check if the host matches one of the trusted domains.
    Subdomains are accepted only if they match an entry in TRUSTED_DOMAINS.
    """
    host = host.lower()
    return any(host == domain or host.endswith("." + domain) for domain in TRUSTED_DOMAINS)

def fetch_image_url(url: str) -> str:
    """
    Resolve and validate an image URL against a whitelist of trusted domains.

    Parameters
    ----------
    url : str
        The raw URL provided by the caller.

    Returns
    -------
    str
        The normalized, verified URL if it passes validation.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP/HTTPS or if the host does not belong to a trusted domain.
    """
    # Basic syntax validation
    parsed: ParseResult = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include scheme and host")

    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP/HTTPS are allowed")

    # Normalize host (remove port if present)
    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a valid hostname")

    if not _is_trusted_domain(host):
        raise ValueError(f"Domain '{host}' is not in the list of trusted hosts")

    # Reconstruct URL to ensure consistent formatting
    normalized = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=host if not parsed.port else f"{host}:{parsed.port}",
    ).geturl()

    return normalized