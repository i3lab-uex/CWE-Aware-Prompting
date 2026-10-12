import urllib.parse

# List of trusted image hosting providers (domain names)
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "images.unsplash.com",
    "picsum.photos",
    "cdn.pixabay.com",
    "flickr.com",
    "images.app.goo.gl",  # Example; adjust as needed
}

def _extract_domain(netloc: str) -> str:
    """
    Extract the registered domain from a network location part of a URL.
    Handles IPv4/IPv6 addresses and removes port numbers if present.
    """
    # Strip any port number
    host = netloc.split(":")[0]
    return host.lower()

def check_image_url(img_address: str) -> str:
    """
    Validate an image URL against a whitelist of trusted domains.

    Parameters
    ----------
    img_address : str
        The URL to validate and potentially normalize.

    Returns
    -------
    str
        The normalized, fully-qualified URL if it passes validation.

    Raises
    ------
    ValueError
        If the scheme is unsupported or the domain is not in the trusted list.
    """
    if not isinstance(img_address, str):
        raise ValueError("img_address must be a string")

    parsed = urllib.parse.urlparse(img_address)

    # Only http and https schemes are allowed
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    domain = _extract_domain(parsed.netloc)
    if domain not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not trusted")

    # Reconstruct the URL to ensure it is fully qualified
    normalized = urllib.parse.urlunparse(parsed)
    return normalized

# Example usage:
if __name__ == "__main__":
    test_urls = [
        "https://i.imgur.com/example.png",
        "http://images.unsplash.com/photo-12345",
        "ftp://imgur.com/image.jpg",  # Should raise ValueError
    ]

    for url in test_urls:
        try:
            print(f"Valid URL: {check_image_url(url)}")
        except ValueError as e:
            print(f"Invalid URL: {url} -> {e}")