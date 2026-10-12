import re
from urllib.parse import urlparse

# List of fully qualified domain names that are considered trustworthy.
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.pixabay.com",
    "i.imgur.com",
    "picsum.photos",
    "images.unsplash.com",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

def validate_picture_url(pic_url: str) -> str:
    """
    Validate that the supplied image URL uses a supported scheme and
    points to one of the trusted domains.  The function returns the URL
    unchanged if it passes validation, otherwise a ValueError is raised.

    Parameters
    ----------
    pic_url : str
        The image URL to validate.

    Returns
    -------
    str
        The original, validated URL.

    Raises
    ------
    ValueError
        If the URL does not use an allowed scheme or its domain is not in
        the trusted list.
    """
    if not isinstance(pic_url, str):
        raise ValueError("pic_url must be a string")

    parsed = urlparse(pic_url)

    # Ensure the scheme is present and allowed
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Normalise the hostname to lower case for comparison
    host = parsed.hostname.lower() if parsed.hostname else ""
    if not host:
        raise ValueError("URL must contain a hostname")

    # Check against the trusted domains list
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain {host!r} is not trusted")

    # Optionally, we can enforce that the URL contains a path component
    if not parsed.path:
        raise ValueError("URL must contain a path to an image")

    # Additional optional checks could be added here, e.g. file extension
    # validation, but for brevity we keep the function minimal.

    return pic_url

# Example usage (commented out for production)
# if __name__ == "__main__":
#     try:
#         valid_url = validate_picture_url("https://i.imgur.com/example.png")
#         print(f"Validated URL: {valid_url}")
#     except ValueError as e:
#         print(f"Validation failed: {e}")