import re
from urllib.parse import urlparse, urljoin

# List of trusted image hosting domains (add or remove as needed)
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "pbs.twimg.com",
    "images.unsplash.com",
    "picsum.photos",
    "cdn.pixabay.com",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

def validate_image_source(img_src: str) -> str:
    """
    Validate that an image URL points to a trusted domain and uses a supported scheme.

    Parameters
    ----------
    img_src : str
        The image URL to validate. May be absolute or relative.

    Returns
    -------
    str
        The fully resolved, validated URL.

    Raises
    ------
    ValueError
        If the URL has an unsupported scheme or points to an untrusted domain.
    """
    if not isinstance(img_src, str) or not img_src.strip():
        raise ValueError("Image source must be a non-empty string")

    # Resolve relative URLs against a dummy base to ensure we can parse them
    resolved_url = urljoin("https://example.com", img_src.strip())
    parsed = urlparse(resolved_url)

    # Check scheme
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}'. Only HTTP/HTTPS are allowed.")

    # Normalize domain (lowercase, strip port)
    host = parsed.hostname or ""
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Remove common subdomain patterns (e.g., www.)
    host = re.sub(r"^www\.", "", host.lower())

    # Verify domain is in the trusted list or its subdomain
    if not any(host == d or host.endswith("." + d) for d in TRUSTED_DOMAINS):
        raise ValueError(f"Untrusted domain '{host}'. Allowed domains: {', '.join(TRUSTED_DOMAINS)}")

    # Reconstruct the URL to ensure it is absolute and canonical
    canonical_url = parsed._replace(fragment="", query="").geturl()
    return canonical_url

# Example usage:
if __name__ == "__main__":
    test_urls = [
        "https://i.imgur.com/abcd1234.jpg",
        "http://pbs.twimg.com/profile_images/abc.png",
        "/images/local_image.png",  # relative URL
        "https://malicious.com/evil.jpg",
        "ftp://imgur.com/file.png",
    ]

    for url in test_urls:
        try:
            print(validate_image_source(url))
        except ValueError as e:
            print(f"Rejected: {e}")