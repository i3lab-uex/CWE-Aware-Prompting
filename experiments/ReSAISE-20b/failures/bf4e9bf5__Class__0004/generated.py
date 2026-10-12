import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (case‑insensitive)
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.safeimg.org",
    "pics.trusted.net",
}

# Regular expression to detect IDNA (punycode) domains
IDNA_PATTERN = re.compile(r"^xn--", re.IGNORECASE)


def _normalize_domain(domain: str) -> str:
    """
    Normalise a domain name for comparison.
    Handles IDNA punycode conversion and lower‑casing.
    """
    # Convert to ASCII (IDNA) if needed
    try:
        domain_ascii = domain.encode("idna").decode("ascii")
    except Exception:
        # If conversion fails, keep original
        domain_ascii = domain

    return domain_ascii.lower()


def resolve_image_url(image_url: str) -> str:
    """
    Resolve an image URL only if it belongs to a trusted domain.

    Parameters
    ----------
    image_url : str
        The URL of the image to validate.

    Returns
    -------
    str
        The original (resolved) URL if it is trusted.

    Raises
    ------
    ValueError
        If the domain of the URL is not in ``TRUSTED_DOMAINS``.
    """
    if not isinstance(image_url, str):
        raise TypeError("image_url must be a string")

    # Parse the URL
    parsed = urlparse(image_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL: missing scheme or host")

    # Normalise domain for comparison
    domain = _normalize_domain(parsed.netloc)

    if domain not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted image host: {domain}")

    # Re‑construct the URL to ensure it is well‑formed
    resolved = urlunparse(parsed)
    return resolved


# Example usage (commented out – remove for production)
if __name__ == "__main__":
    try:
        print(resolve_image_url("https://images.example.com/photo.jpg"))
        # This will raise ValueError
        print(resolve_image_url("https://malicious.com/evil.png"))
    except Exception as e:
        print(e)