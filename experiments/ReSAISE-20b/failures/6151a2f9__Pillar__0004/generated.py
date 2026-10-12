import urllib.parse

# Trusted image hosting providers (domain names only, no subdomains)
_TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "picsum.photos",
    "cdn.pixabay.com",
    "flickr.com",
    "twitpic.com",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}


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
        The original URL if it is considered safe and trusted.

    Raises
    ------
    ValueError
        If the URL scheme is unsupported, or if the host does not belong to
        the trusted domain list.
    """
    # Parse the URL
    parsed = urllib.parse.urlparse(pic_url)

    # Check scheme
    if parsed.scheme not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Extract host and compare against trusted list
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Normalize host to lowercase for comparison
    hostname = hostname.lower()

    if hostname not in _TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {hostname}")

    # Reconstruct the URL to ensure it is canonical
    cleaned_url = urllib.parse.urlunparse(parsed)

    return cleaned_url