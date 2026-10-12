import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains.
_TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "cdn.example.com",   # replace with actual trusted domains
}

# Allowed URL schemes.
_ALLOWED_SCHEMES = {"http", "https"}

def _is_trusted_domain(netloc: str) -> bool:
    """
    Check whether the netloc belongs to a trusted domain.
    Subdomains are allowed if they end with a trusted domain.
    """
    # Normalize the netloc by removing port number
    host = netloc.split(":")[0].lower()
    return any(host == domain or host.endswith("." + domain) for domain in _TRUSTED_DOMAINS)

def fetch_image_url(img_url: str) -> str:
    """
    Validate an image URL and return the canonical URL if it is from a trusted domain.

    Parameters
    ----------
    img_url : str
        The image URL to validate and resolve.

    Returns
    -------
    str
        The validated, canonical URL.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https, or if the domain is not trusted.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    parsed = urlparse(img_url)

    # Ensure scheme is allowed
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure domain is trusted
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.netloc}")

    # Rebuild the URL to canonical form (lowercase scheme & host, remove default ports)
    netloc = parsed.netloc
    if ":" in netloc:
        host, port = netloc.split(":", 1)
        # Remove default ports for http/https
        if (parsed.scheme.lower() == "http" and port == "80") or \
           (parsed.scheme.lower() == "https" and port == "443"):
            netloc = host

    canonical = urlunparse((
        parsed.scheme.lower(),
        netloc,
        parsed.path or "",
        "",  # params
        parsed.query,   # preserve query string if present
        ""  # fragment
    ))
    return canonical