import re
from urllib.parse import urlparse

# Whitelisted domains for image hosting services
_TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "picsum.photos",
    "placekitten.com",
}

# Regular expression to validate a URL scheme
_SCHEME_REGEX = re.compile(r"^(https?)://", re.IGNORECASE)


def fetch_image_url(url: str) -> str:
    """
    Validate that the given image URL uses a trusted domain and an allowed scheme.

    Parameters
    ----------
    url : str
        The URL of the image to resolve.

    Returns
    -------
    str
        The verified image URL if it belongs to a trusted domain.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https or if the domain is not trusted.
    """
    # Basic scheme check
    match = _SCHEME_REGEX.match(url)
    if not match:
        raise ValueError("URL must start with http:// or https://")

    # Parse the URL to extract components
    parsed = urlparse(url)

    # Ensure host is present
    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    # Normalize the host (lowercase, strip leading/trailing dots)
    host = parsed.hostname.lower().strip(".")

    # Verify domain is in the trusted list
    if host not in _TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted image domain: {host}")

    # Reconstruct the URL to ensure canonical form
    verified_url = parsed.geturl()

    return verified_url


# Example usage (commented out; remove comments to test)
# if __name__ == "__main__":
#     try:
#         print(fetch_image_url("https://i.imgur.com/example.png"))
#     except ValueError as e:
#         print(f"Validation error: {e}")