import urllib.parse

# List of trusted image hosting domains.
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trusted.com",
    "img.safe-host.org",
}

# Allowed URL schemes.
ALLOWED_SCHEMES = {"http", "https"}


def fetch_image_url(img_url: str) -> str:
    """
    Validate that the provided image URL belongs to a trusted domain and uses an allowed scheme.

    Parameters
    ----------
    img_url : str
        The image URL to validate and resolve.

    Returns
    -------
    str
        The validated, absolute URL.

    Raises
    ------
    ValueError
        If the URL has an unsupported scheme, is not absolute, or its domain is untrusted.
    """
    # Parse the URL and validate scheme
    parsed = urllib.parse.urlparse(img_url)
    if not parsed.scheme or parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Ensure the URL is absolute (has netloc)
    if not parsed.netloc:
        raise ValueError("URL must be absolute and contain a network location")

    # Normalize domain (lowercase, strip port if present)
    hostname = parsed.hostname.lower()
    if hostname not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {hostname!r}")

    # Rebuild the URL to ensure it is canonical
    normalized_url = urllib.parse.urlunparse(parsed._replace(fragment=""))
    return normalized_url