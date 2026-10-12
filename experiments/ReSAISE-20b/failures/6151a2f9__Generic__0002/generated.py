import re
from urllib.parse import urlparse, urlunparse

# A minimal list of trusted image hosting providers.
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "images.unsplash.com",
    "picsum.photos",
    "cdn.pixabay.com",
}

# Allowed URL schemes.
ALLOWED_SCHEMES = {"http", "https"}


def _canonical_host(host: str) -> str:
    """
    Normalize the host by stripping any port number.
    """
    return host.split(":")[0].lower()


def _is_trusted_host(host: str) -> bool:
    """
    Check whether the given host is in the trusted list.
    Subdomains are accepted if they end with a known trusted domain.
    """
    host = _canonical_host(host)
    for domain in TRUSTED_DOMAINS:
        if host == domain or host.endswith("." + domain):
            return True
    return False


def validate_picture_url(pic_url: str) -> str:
    """
    Validate an image URL against a list of trusted domains.

    Parameters
    ----------
    pic_url : str
        The input image URL to validate.

    Returns
    -------
    str
        The canonical, fully resolved URL if it is valid.

    Raises
    ------
    ValueError
        If the URL scheme is not supported or if the domain is not trusted.
    """
    # Basic validation of input type
    if not isinstance(pic_url, str):
        raise ValueError("pic_url must be a string")

    # Parse the URL
    parsed = urlparse(pic_url)

    # Validate scheme
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate host
    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    if not _is_trusted_host(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.netloc}")

    # Reconstruct the URL to ensure it is in a canonical form
    canonical = urlunparse(
        (
            parsed.scheme.lower(),
            _canonical_host(parsed.netloc),
            parsed.path,
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return canonical