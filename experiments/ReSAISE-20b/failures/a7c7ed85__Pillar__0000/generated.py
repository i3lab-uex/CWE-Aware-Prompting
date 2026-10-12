import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (case‑insensitive)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "i.imgur.com",
    "picsum.photos",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}


def _normalize_domain(host: str) -> str:
    """
    Normalise the host by stripping common prefixes like 'www.'.
    """
    return re.sub(r"^www\.", "", host.lower())


def validate_image_url(img_url: str) -> str:
    """
    Validate that an image URL belongs to a trusted domain and uses a supported scheme.

    Parameters
    ----------
    img_url : str
        The input image URL to validate.

    Returns
    -------
    str
        The fully resolved, canonical URL if it passes validation.

    Raises
    ------
    ValueError
        If the URL scheme is unsupported or the host is not in the trusted list.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    parsed = urlparse(img_url)

    # Scheme check
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Domain check
    host = _normalize_domain(parsed.netloc)
    if host not in _TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {host}")

    # Re‑build the URL to ensure it is canonical
    canonical = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return canonical