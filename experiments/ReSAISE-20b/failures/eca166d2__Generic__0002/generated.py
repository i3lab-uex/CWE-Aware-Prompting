import urllib.parse

# List of trusted image hosting domains (add or remove as needed)
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "picsum.photos",
    "cdn.pixabay.com",
    "upload.wikimedia.org",
}

def validate_image_source(img_src: str) -> str:
    """
    Validate that the provided image URL is from a trusted provider.

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
        If the URL has an unsupported scheme, is malformed,
        or points to an untrusted domain.
    """
    if not isinstance(img_src, str):
        raise ValueError("Image source must be a string")

    # Parse the URL
    parsed = urllib.parse.urlparse(img_src.strip())

    # Ensure scheme is http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure netloc (domain) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    # Normalize the domain to lower case for comparison
    domain = parsed.netloc.lower()

    # Check if the domain is trusted or a subdomain of a trusted domain
    if not any(domain == d or domain.endswith("." + d) for d in TRUSTED_DOMAINS):
        raise ValueError(f"Untrusted image domain: {domain}")

    # Reconstruct the URL to ensure it is fully qualified
    validated_url = urllib.parse.urlunparse(parsed)

    return validated_url