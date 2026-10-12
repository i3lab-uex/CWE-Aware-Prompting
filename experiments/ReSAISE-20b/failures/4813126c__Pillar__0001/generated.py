import urllib.parse

# List of domains that are considered trusted image hosts.
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "i.redd.it",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "picsum.photos",
}

def verify_image_url(img_url: str) -> str:
    """
    Validate an image URL against a whitelist of trusted domains.

    Parameters
    ----------
    img_url : str
        The URL to validate and potentially resolve.

    Returns
    -------
    str
        The original URL if it is deemed trustworthy.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https or if its domain is not in
        :data:`TRUSTED_DOMAINS`.
    """
    # Parse the URL into components
    parsed = urllib.parse.urlparse(img_url)

    # Scheme must be http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Normalize the domain (remove port if present)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Check that the host is in the trusted list
    if hostname.lower() not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {hostname!r}")

    # Reconstruct the URL to ensure consistent formatting
    verified = urllib.parse.urlunparse(parsed)
    return verified