import re
from urllib.parse import urlparse, urlunparse

# A list of trusted image hosting domains (case‑insensitive)
_TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trustedhost.org",
    "pics.safe-site.net",
    # Add more domains as needed
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}


def get_image_link(link_image: str) -> str:
    """
    Validate that the supplied image URL points to a trusted domain and uses an allowed scheme.
    Returns the original, fully‑qualified URL if validation passes.

    Parameters
    ----------
    link_image : str
        The image URL to validate and resolve.

    Returns
    -------
    str
        The validated, resolved URL.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, is not absolute,
        or does not belong to a trusted domain.
    """
    if not isinstance(link_image, str):
        raise ValueError("link_image must be a string")

    # Parse the URL
    parsed = urlparse(link_image)

    # Ensure we have a scheme and netloc (i.e., absolute URL)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute and include a scheme")

    # Normalize the scheme to lower case
    scheme = parsed.scheme.lower()
    if scheme not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}'. Only http and https are allowed")

    # Normalize the domain (lower case) and strip possible port
    hostname = parsed.hostname.lower() if parsed.hostname else ""
    # Remove leading 'www.' for comparison
    hostname = re.sub(r"^www\.", "", hostname)

    if hostname not in _TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain '{hostname}'. Allowed domains are: {', '.join(_TRUSTED_DOMAINS)}")

    # Re‑build the URL to ensure consistent formatting
    cleaned = parsed._replace(scheme=scheme, netloc=f"{hostname}{':' + str(parsed.port) if parsed.port else ''}")
    return urlunparse(cleaned)