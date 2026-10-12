import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (add as needed)
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.example.org",
    "img.host.com",
}

# Allowed schemes
ALLOWED_SCHEMES = {"http", "https"}


def _normalize_domain(domain: str) -> str:
    """
    Normalise a domain name by stripping common prefixes such as 'www.'.
    """
    return re.sub(r"^www\.", "", domain.lower())


def check_image_url(img_address: str) -> str:
    """
    Validate that the supplied image URL is hosted on a trusted domain and uses
    an allowed scheme. Returns the fully resolved, normalised URL if valid.

    Parameters
    ----------
    img_address : str
        The image URL to validate.

    Returns
    -------
    str
        Normalised, fully resolved URL that is safe to use.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https or if the domain is not in the trusted list.
    """
    if not isinstance(img_address, str):
        raise ValueError("img_address must be a string")

    parsed = urlparse(img_address)

    # Scheme check
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Domain check
    domain = _normalize_domain(parsed.netloc)
    if domain not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not trusted")

    # Reconstruct the URL to ensure consistent formatting
    normalized = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc,
        parsed.path,
        parsed.params,
        parsed.query,
        parsed.fragment
    ))

    return normalized