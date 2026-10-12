import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (case‑insensitive)
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "images.example.com",  # replace with your own trusted domains
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


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
        The normalized, fully resolved URL if the domain is trusted.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, contains credentials,
        or does not belong to a trusted domain.
    """

    # Basic sanity check: URL must be non‑empty and contain at least a scheme
    if not link_image or not isinstance(link_image, str):
        raise ValueError("link_image must be a non‑empty string")

    # Parse the URL
    parsed = urlparse(link_image)

    # Scheme must be http or https
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Reject URLs that contain userinfo (e.g., http://user:pass@host)
    if parsed.username or parsed.password:
        raise ValueError("URL must not contain credentials")

    # Normalize the hostname to lowercase
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Ensure the host ends with a trusted domain
    if not any(host == td or host.endswith("." + td) for td in TRUSTED_DOMAINS):
        raise ValueError(f"Untrusted domain: {host}")

    # Re‑assemble the URL to ensure it is normalized (no fragments, etc.)
    safe_parts = (
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        "",  # no fragment
    )
    resolved_url = urlunparse(safe_parts)

    return resolved_url


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    test_urls = [
        "https://i.imgur.com/abcd1234.png",
        "http://images.example.com/gallery/pic.jpg?size=large",
        "https://malicious.com/evil.png",
        "ftp://i.imgur.com/file.jpg",
    ]

    for url in test_urls:
        try:
            print(f"Valid: {get_image_link(url)}")
        except ValueError as e:
            print(f"Invalid: {url} -> {e}")