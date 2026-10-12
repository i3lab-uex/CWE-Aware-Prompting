import urllib.parse

# List of fully-qualified domains that are considered trusted.
_TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trustedhost.org",
    "assets.safe-site.net",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}


def validate_image_source(img_src: str) -> str:
    """
    Validate that the supplied image URL comes from a trusted domain and uses an
    allowed scheme. Returns the fully-qualified URL if valid, otherwise raises
    ValueError.

    Parameters
    ----------
    img_src : str
        The image URL to validate and resolve.

    Returns
    -------
    str
        The validated, fully-qualified image URL.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme, or points to an
        untrusted domain.
    """
    if not isinstance(img_src, str) or not img_src:
        raise ValueError("Image source must be a non-empty string")

    # Parse the URL
    parsed = urllib.parse.urlparse(img_src)

    # Ensure scheme is present and allowed
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Resolve relative URLs by assuming the caller provides a full absolute URL.
    # If you need to support relative paths, you must supply a base URL context
    # which is outside the scope of this function.

    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a hostname")

    # Normalise the host (e.g., remove leading/trailing whitespace, lower-case)
    host = host.strip().lower()

    # Check if the host is in the trusted list
    if host not in _TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {host}")

    # Rebuild the URL to ensure consistency (e.g., no duplicate slashes)
    normalized_url = urllib.parse.urlunparse(parsed)

    return normalized_url