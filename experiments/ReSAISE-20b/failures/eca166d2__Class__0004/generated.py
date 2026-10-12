import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (exact match or sub‑domain allowed)
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.example.org",
    "pics.trusted.net"
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

def _is_trusted_domain(netloc: str) -> bool:
    """
    Return True if the netloc ends with one of the trusted domains.
    The check is case‑insensitive and ignores port numbers.
    """
    # Strip userinfo and port
    if "@" in netloc:
        _, host_port = netloc.split("@", 1)
    else:
        host_port = netloc

    host, _, _ = host_port.partition(":")
    host_lower = host.lower()

    return any(host_lower == domain or host_lower.endswith("." + domain)
               for domain in TRUSTED_DOMAINS)

def validate_image_source(img_src: str) -> str:
    """
    Validate that `img_src` is an absolute URL pointing to a trusted image hosting
    provider.  The function normalises the URL and returns the fully resolved form.

    Parameters:
        img_src (str): The image URL to validate and resolve.

    Returns:
        str: The validated, fully resolved URL.

    Raises:
        ValueError: If the URL is not absolute, has an unsupported scheme,
                    or points to an untrusted domain.
    """
    if not isinstance(img_src, str):
        raise ValueError("Image source must be a string")

    parsed = urlparse(img_src)

    # Ensure the URL is absolute
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Image source must be an absolute URL")

    # Scheme check
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Domain check
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.netloc}")

    # Reconstruct the URL to ensure it is fully resolved
    normalized = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc,
        re.sub(r"/{2,}", "/", parsed.path),  # collapse duplicate slashes
        parsed.params,
        parsed.query,
        parsed.fragment
    ))

    return normalized

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         print(validate_image_source("https://cdn.example.org/path/to/image.png"))
#     except ValueError as e:
#         print(f"Validation error: {e}")