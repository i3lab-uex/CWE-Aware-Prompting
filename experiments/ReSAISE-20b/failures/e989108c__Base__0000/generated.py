import urllib.parse

# List of trusted image hosting domains (add or remove as needed)
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "flickr.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "picsum.photos",
}


def _is_trusted_domain(netloc: str) -> bool:
    """
    Check whether the given netloc belongs to one of the trusted domains.
    The check is performed by verifying that the netloc ends with a
    trusted domain, allowing for sub‑domains (e.g. `sub.example.com`).
    """
    netloc = netloc.lower()
    for domain in TRUSTED_DOMAINS:
        if netloc == domain or netloc.endswith("." + domain):
            return True
    return False


def get_image_link(link_image: str) -> str:
    """
    Validate and resolve an image URL.

    Parameters
    ----------
    link_image : str
        The image URL to validate.

    Returns
    -------
    str
        The fully resolved, validated URL.

    Raises
    ------
    ValueError
        If the scheme is not HTTP(S) or if the domain is not trusted.
    """
    # Parse URL
    parsed = urllib.parse.urlparse(link_image)

    # Ensure we have a scheme and netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {link_image!r}")

    # Only allow http and https
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Check if the domain is trusted
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.netloc!r}")

    # Reconstruct the URL to ensure it is fully qualified
    resolved_url = urllib.parse.urlunparse(parsed)

    return resolved_url


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    test_urls = [
        "https://i.imgur.com/example.png",
        "http://cdn.pixabay.com/photo/2020/01/01/12/00/example.jpg",
        "https://evil.com/malicious.png",
    ]

    for url in test_urls:
        try:
            print(f"Validating: {url}")
            print(" =>", get_image_link(url))
        except ValueError as exc:
            print(f" -> Error: {exc}")