import urllib.parse

# List of domains considered trusted for image hosting.
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trusted.com",
    "secure.images.org",
    # Add more trusted domains as needed.
}

def resolve_image_url(image_url: str) -> str:
    """
    Validate that an image URL belongs to a trusted domain and return the
    resolved absolute URL.

    Parameters:
        image_url (str): The input image URL.

    Returns:
        str: The validated and normalized absolute URL.

    Raises:
        ValueError: If the URL's domain is not in TRUSTED_DOMAINS.
        ValueError: If the input is not a valid absolute URL.
    """
    # Parse the URL and ensure it has a scheme and network location
    parsed = urllib.parse.urlparse(image_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL: missing scheme or netloc")

    # Normalize the domain (lowercase) and strip port if present
    hostname = parsed.hostname.lower() if parsed.hostname else ""
    if not hostname:
        raise ValueError("Invalid URL: missing host")

    # Check against trusted domains
    if hostname not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {hostname}")

    # Reconstruct the URL to ensure it is absolute and normalized
    # (e.g., remove fragment, normalize path)
    resolved = urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        urllib.parse.normpath(parsed.path),
        parsed.params,
        parsed.query,
        ""  # drop fragment
    ))
    return resolved