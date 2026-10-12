import re
from urllib.parse import urlparse, urlunparse

# List of trusted domains.  Subdomains are allowed if they match the pattern.
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.somehost.org",
    "trusted-photos.net",
}

# Regex to match supported schemes (http and https)
SCHEME_REGEX = re.compile(r"^(https?)$")

def _is_trusted_domain(host: str) -> bool:
    """
    Check if the given host matches one of the trusted domains.
    Subdomains are accepted only when the base domain is in TRUSTED_DOMAINS.
    """
    # Normalize host to lowercase
    host = host.lower()
    if host in TRUSTED_DOMAINS:
        return True

    # Check for subdomain: e.g., sub.images.example.com
    parts = host.split(".")
    if len(parts) < 3:
        return False

    # Reconstruct base domain (last two parts)
    base_domain = ".".join(parts[-2:])
    return base_domain in TRUSTED_DOMAINS


def validate_image_source(img_src: str) -> str:
    """
    Validate that `img_src` is a fully-qualified URL pointing to an image hosted
    on one of the trusted domains.  The function accepts only http/https schemes.

    Parameters
    ----------
    img_src : str
        The image URL to validate and resolve.

    Returns
    -------
    str
        The normalized, fully-qualified image URL if it is trusted.

    Raises
    ------
    ValueError
        If the URL has an unsupported scheme, is missing a host,
        or points to an untrusted domain.
    """
    if not isinstance(img_src, str):
        raise ValueError("img_src must be a string")

    # Parse the URL
    parsed = urlparse(img_src)

    # Scheme must be http or https
    if not SCHEME_REGEX.match(parsed.scheme):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Host must be present
    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    # Validate domain
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.netloc!r}")

    # Reconstruct the URL to ensure consistent formatting
    normalized = urlunparse(parsed._replace(fragment=""))
    return normalized

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    test_urls = [
        "https://images.example.com/photo.jpg",
        "http://sub.images.example.com/another.png",
        "https://untrusted.com/img.png",
        "ftp://images.example.com/file.jpg",
    ]

    for url in test_urls:
        try:
            print(f"Valid: {validate_image_source(url)}")
        except ValueError as exc:
            print(f"Invalid: {url} -> {exc}")