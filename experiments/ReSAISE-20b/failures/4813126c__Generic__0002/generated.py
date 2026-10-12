import urllib.parse

# List of trusted image hosting domains.
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "placekitten.com",
    "picsum.photos",
}

def verify_image_url(img_url: str) -> str:
    """
    Verify that an image URL belongs to a trusted domain and uses
    a supported scheme (http or https).

    Parameters
    ----------
    img_url : str
        The URL of the image to resolve.

    Returns
    -------
    str
        The verified image URL if it is trusted.

    Raises
    ------
    ValueError
        If the scheme is not http/https or if the domain is not trusted.
    """
    # Parse the URL and ensure it has a scheme and network location
    parsed = urllib.parse.urlparse(img_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {img_url!r}")

    # Only allow http and https schemes
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme {parsed.scheme!r} in URL: {img_url!r}")

    # Normalize the netloc (remove port if present)
    host = parsed.hostname
    if host is None:
        raise ValueError(f"Could not determine hostname in URL: {img_url!r}")

    # Check if the host is in the trusted list
    if host.lower() not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain {host!r} is not trusted for image URLs")

    # Reconstruct the URL to avoid any malicious fragments or query tricks
    safe_url = urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        "",  # params
        "",  # query
        ""   # fragment
    ))
    return safe_url