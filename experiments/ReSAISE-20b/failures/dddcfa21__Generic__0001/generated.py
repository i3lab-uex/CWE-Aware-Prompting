import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (add or remove as needed)
_TRUSTED_DOMAINS = {
    "images.unsplash.com",
    "i.imgur.com",
    "cdn.pixabay.com",
    "picsum.photos",
    "res.cloudinary.com",
    "images.pexels.com",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}


def _is_trusted_domain(domain: str) -> bool:
    """
    Check if the given domain is in the trusted list.
    Subdomains are allowed only if explicitly listed.
    """
    return domain.lower() in _TRUSTED_DOMAINS


def check_image_url(img_address: str) -> str:
    """
    Validate that `img_address` points to a trusted image hosting domain
    and uses an allowed scheme.  The function returns the fully resolved URL.

    Parameters
    ----------
    img_address : str
        Input image URL to validate.

    Returns
    -------
    str
        The validated, fully resolved URL.

    Raises
    ------
    ValueError
        If the scheme is unsupported, or if the domain is not in the trusted list.
    """
    if not isinstance(img_address, str):
        raise ValueError("img_address must be a string")

    # Parse the URL
    parsed = urlparse(img_address)

    # Ensure scheme is present and allowed
    if not parsed.scheme:
        raise ValueError("URL must include a scheme (http or https)")
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure netloc (domain) is present
    if not parsed.netloc:
        raise ValueError("URL must include a domain")

    # Strip port if present for comparison
    domain = parsed.hostname or ""
    if not _is_trusted_domain(domain):
        raise ValueError(f"Domain '{domain}' is not in the trusted list")

    # Reconstruct the URL to ensure it is fully qualified
    normalized = urlunparse(parsed._replace(scheme=parsed.scheme.lower(),
                                            netloc=domain))
    return normalized