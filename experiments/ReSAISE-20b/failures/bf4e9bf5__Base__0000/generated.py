import urllib.parse

# List of trusted image hosting domains (add more as needed)
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "pics.flickr.com",
    "cdn.pixabay.com",
    "storage.googleapis.com",
}

def resolve_image_url(image_url: str) -> str:
    """
    Resolve an image URL by validating that its domain is in the trusted list.

    Parameters
    ----------
    image_url : str
        The image URL to be resolved.

    Returns
    -------
    str
        The original image_url if it belongs to a trusted domain.

    Raises
    ------
    ValueError
        If the URL's domain is not in TRUSTED_DOMAINS or if the URL scheme is unsupported.
    """
    # Parse the URL
    parsed = urllib.parse.urlparse(image_url)

    # Ensure scheme is HTTP(S) to avoid other protocols (ftp, file, etc.)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalize the domain to lower case
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Check against the trusted list
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted image domain: {host}")

    # If all checks pass, return the original URL (or you could rebuild it)
    return image_url