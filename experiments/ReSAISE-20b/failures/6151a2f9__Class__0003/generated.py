import re
from urllib.parse import urlparse, urlunparse

# List of domains that are considered trusted image hosts.
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trustedsite.org",
    "pics.safe-host.net",
    # Add more trusted domains here as needed.
}

# Allowed URL schemes for image URLs.
ALLOWED_SCHEMES = {"http", "https"}

def _is_trusted_domain(domain: str) -> bool:
    """
    Check if the provided domain or any of its parent domains
    are present in the TRUSTED_DOMAINS set.
    """
    # Normalize to lowercase and strip port if present
    domain = domain.split(":")[0].lower()
    # A simple check: exact match or subdomain of a trusted domain
    for trusted in TRUSTED_DOMAINS:
        if domain == trusted or domain.endswith("." + trusted):
            return True
    return False

def validate_picture_url(pic_url: str) -> str:
    """
    Validate that a picture URL uses an allowed scheme and comes from a
    trusted image host domain.

    Parameters
    ----------
    pic_url : str
        The input image URL to validate.

    Returns
    -------
    str
        The normalized, validated URL.

    Raises
    ------
    ValueError
        If the scheme is unsupported or the domain is not trusted.
    """
    if not isinstance(pic_url, str):
        raise ValueError("pic_url must be a string")

    # Parse the URL
    parsed = urlparse(pic_url)

    # Ensure scheme is allowed
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure netloc (domain) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    # Verify the domain is trusted
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.netloc}")

    # Reconstruct the URL to ensure it is canonical
    normalized = urlunparse(parsed._replace(fragment=""))

    # Optional: ensure no query parameters that could lead to unintended
    # content loading (e.g., image manipulation queries). For stricter
    # policies, you could whitelist acceptable query keys.
    return normalized

# Example usage:
if __name__ == "__main__":
    try:
        url = validate_picture_url("https://images.example.com/path/to/image.jpg")
        print(f"Validated URL: {url}")
    except ValueError as e:
        print(f"Validation failed: {e}")