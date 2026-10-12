import re
from urllib.parse import urlparse, urlunparse

# List of approved image hosting domains (can be extended)
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.redd.it",
    "cdn.example.com",   # replace with actual trusted domains
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def fetch_image_url(img_url: str) -> str:
    """
    Validate that the supplied image URL points to a trusted domain and uses an allowed
    scheme.  If valid, return the fully qualified URL.

    Parameters
    ----------
    img_url : str
        The image URL to validate and resolve.

    Returns
    -------
    str
        The validated, fully qualified image URL.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https or if the domain is untrusted.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    # Parse the URL
    parsed = urlparse(img_url)

    # Ensure scheme is allowed
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Ensure netloc (domain) is trusted
    domain = parsed.hostname or ""
    if not any(domain == d or domain.endswith("." + d) for d in TRUSTED_DOMAINS):
        raise ValueError(f"Untrusted domain: {domain!r}")

    # Reconstruct the URL to ensure it's fully qualified
    resolved = urlunparse(parsed)

    return resolved


# Example usage (commented out to keep the module importable without side effects)
if __name__ == "__main__":
    test_urls = [
        "https://i.redd.it/abcd1234.png",
        "http://imgur.com/gallery/xyz.jpg",
        "https://cdn.example.com/path/to/image.jpeg",
        "ftp://malicious.com/evil.png",
        "https://untrusted.com/image.jpg",
    ]

    for url in test_urls:
        try:
            print(f"Valid: {fetch_image_url(url)}")
        except ValueError as e:
            print(f"Invalid: {url} -> {e}")