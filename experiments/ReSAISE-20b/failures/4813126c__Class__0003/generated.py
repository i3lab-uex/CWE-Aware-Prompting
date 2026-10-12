import re
from urllib.parse import urlparse, ParseResult

# List of trusted image hosting domains (case‑insensitive)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "images.unsplash.com",
    "pbs.twimg.com",
    "cdn.discordapp.com",
    # Add more domains as needed
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}

def _is_trusted_domain(host: str) -> bool:
    """
    Check whether the host matches any trusted domain or its subdomain.
    Comparison is case‑insensitive and does not allow trailing dots.
    """
    host = host.lower().rstrip(".")
    for domain in _TRUSTED_DOMAINS:
        if host == domain or host.endswith("." + domain):
            return True
    return False

def verify_image_url(img_url: str) -> str:
    """
    Validate that an image URL belongs to a trusted domain and uses a
    recognized scheme.  The function returns the original URL if it passes
    all checks; otherwise, a ValueError is raised.

    Parameters
    ----------
    img_url : str
        The URL to validate.

    Returns
    -------
    str
        The validated image URL unchanged.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        or its domain is not in the trusted list.
    """
    if not isinstance(img_url, str):
        raise ValueError("Image URL must be a string")

    # Basic syntax check
    try:
        parsed: ParseResult = urlparse(img_url)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Malformed URL: {img_url}") from exc

    # Scheme validation
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http/https are allowed")

    # Netloc (host) validation
    if not parsed.netloc:
        raise ValueError("URL must contain a host component")

    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted host: {parsed.netloc}")

    # Optional: enforce that the path ends with a common image extension
    if not re.search(r"\.(jpg|jpeg|png|gif|webp)$", parsed.path, re.IGNORECASE):
        raise ValueError("URL does not point to a recognized image file")

    return img_url