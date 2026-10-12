import urllib.parse

# List of trusted image hosting domains.
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "flickr.com",
    "i.redd.it",
    # Add more domains as needed.
}

def verify_image_url(img_url: str) -> str:
    """
    Validate that an image URL belongs to a trusted domain.

    Parameters
    ----------
    img_url : str
        The absolute URL of the image to be verified.

    Returns
    -------
    str
        The original URL if it is valid and trusted.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP/HTTPS, or if the domain is not in the trusted list.
    """
    # Parse the URL to inspect components
    parsed = urllib.parse.urlparse(img_url)

    # Scheme must be http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Domain must be present
    if not parsed.netloc:
        raise ValueError("URL does not contain a network location (domain)")

    # Normalize domain to lowercase for comparison
    host = parsed.netloc.lower()

    # Strip port if present
    if ":" in host:
        host = host.split(":")[0]

    # Check against the trusted domain list
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not trusted")

    # Reconstruct the URL to ensure consistent formatting
    verified_url = urllib.parse.urlunparse(parsed)

    return verified_url