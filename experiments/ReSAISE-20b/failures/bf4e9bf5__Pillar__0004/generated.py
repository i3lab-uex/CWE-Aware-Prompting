import urllib.parse

# List of trusted image hosting domains.
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "static.wikia.nocookie.net",
    "images.pexels.com",
}


def resolve_image_url(image_url: str) -> str:
    """
    Resolve an image URL after verifying that its domain is trusted.

    Parameters
    ----------
    image_url : str
        The image URL to be resolved.

    Returns
    -------
    str
        The original URL if it belongs to a trusted domain.

    Raises
    ------
    ValueError
        If the URL's domain is not in the trusted list.
    """
    if not isinstance(image_url, str):
        raise TypeError("image_url must be a string")

    parsed = urllib.parse.urlparse(image_url)

    # Ensure the URL has a scheme and netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL: missing scheme or network location")

    # Normalize the domain (lowercase, strip port if present)
    netloc = parsed.netloc.lower()
    # Remove IPv6 brackets and split off the port if present
    if netloc.startswith("["):
        # IPv6 literal: [2001:db8::1]:80
        host_part = netloc.split("]")[0][1:]
    else:
        host_part = netloc.split(":")[0]

    # Check against the trusted domains set
    if host_part not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host_part}' is not trusted")

    # Reconstruct the URL to ensure consistent formatting
    resolved_url = urllib.parse.urlunparse(parsed)
    return resolved_url