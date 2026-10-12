import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains.
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "flickr.com",
    "postimg.cc",
    "imgur.com",
}

# Allowed URL schemes.
ALLOWED_SCHEMES = {"http", "https"}


def validate_image_url(img_url: str) -> str:
    """
    Validate an image URL against a list of trusted domains.

    Parameters
    ----------
    img_url : str
        The image URL to validate.

    Returns
    -------
    str
        The fully resolved and validated URL.

    Raises
    ------
    ValueError
        If the scheme is not supported or the domain is not trusted.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    # Parse the URL.
    parsed = urlparse(img_url)

    # Validate scheme.
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalize the hostname to lower case for comparison.
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Check the domain against the trusted list.
    # Support subdomains of the trusted domains as well.
    if not any(
        host == domain or host.endswith("." + domain) for domain in TRUSTED_DOMAINS
    ):
        raise ValueError(f"Domain '{host}' is not trusted")

    # Reconstruct the URL to ensure it has a path.
    # If no path is provided, default to '/' to avoid empty URLs.
    path = parsed.path or "/"

    # Remove query and fragment for a clean image URL
    cleaned_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            path,
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return cleaned_url


# Example usage (uncomment to test):
# print(validate_image_url("https://i.imgur.com/abcd1234.jpg"))