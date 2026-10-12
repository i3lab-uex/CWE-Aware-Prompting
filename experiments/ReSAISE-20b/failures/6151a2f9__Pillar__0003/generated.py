import urllib.parse

# List of trusted image host domains (case‑insensitive).
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "cdn.example.com",      # add your own trusted hosts here
    "images.unsplash.com",
}

def validate_picture_url(pic_url: str) -> str:
    """
    Validate an image URL and return the fully resolved URL if it belongs to a trusted domain.

    Parameters
    ----------
    pic_url : str
        The input image URL to validate.

    Returns
    -------
    str
        The fully resolved, normalized URL if it is valid and trusted.

    Raises
    ------
    ValueError
        If the URL scheme is unsupported or the domain is not in the trusted list.
    """
    if not isinstance(pic_url, str):
        raise ValueError("pic_url must be a string")

    # Parse the URL
    parsed = urllib.parse.urlparse(pic_url)

    # Ensure we have a scheme and netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include a scheme and domain")

    # Only allow http or https
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalize the domain to lowercase for comparison
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Check against the trusted domains list
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not trusted")

    # Rebuild the URL to ensure consistent formatting (e.g., no duplicate slashes)
    normalized = urllib.parse.urlunparse((
        parsed.scheme.lower(),
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))

    return normalized