import re
from urllib.parse import urlparse

# List of domains that are allowed to host images.
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.pixabay.com",
    "i.imgur.com",
    "picsum.photos",
    "images.unsplash.com",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

def _is_valid_domain(domain: str) -> bool:
    """
    Check if the provided domain (or any of its parent domains)
    is present in the TRUSTED_DOMAINS set.
    """
    # Normalize subdomains: e.g., a.b.c.com -> c.com
    parts = domain.lower().split(".")
    for i in range(len(parts) - 1):
        candidate = ".".join(parts[i:])
        if candidate in TRUSTED_DOMAINS:
            return True
    return False


def validate_image_url(img_url: str) -> str:
    """
    Validate that the supplied image URL points to a trusted domain
    and uses an allowed scheme (http/https). Return the normalized URL.

    Parameters
    ----------
    img_url : str
        The image URL to validate.

    Returns
    -------
    str
        The original (or normalized) URL if it is valid.

    Raises
    ------
    ValueError
        If the scheme is not http/https or if the domain is not trusted.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    # Parse the URL
    parsed = urlparse(img_url)

    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain)")

    # Basic hostname validation: no IP addresses or port numbers
    # Reject URLs that use IPv4/IPv6 literals
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", parsed.netloc) or re.match(r"^\[.*\]$", parsed.netloc):
        raise ValueError("IP addresses are not allowed in image URLs")

    # Strip any port number for domain validation
    host = parsed.hostname.lower()
    if not _is_valid_domain(host):
        raise ValueError(f"Domain '{host}' is not in the trusted list")

    # Reconstruct the URL to ensure consistent formatting
    normalized_url = parsed.geturl()
    return normalized_url


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         print(validate_image_url("https://i.imgur.com/abcd1234.png"))
#     except ValueError as e:
#         print(f"Validation failed: {e}")