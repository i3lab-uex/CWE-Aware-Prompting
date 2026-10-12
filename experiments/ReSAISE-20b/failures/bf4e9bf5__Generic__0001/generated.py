import re
from urllib.parse import urlparse, urlunparse

# List of domains that are considered trusted image hosts
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "picsum.photos",
    "flickr.com",
}

# Regular expression to validate the URL format
URL_REGEX = re.compile(
    r"^(?P<scheme>https?)://"
    r"(?P<host>[a-zA-Z0-9.-]+)"
    r"(?::\d+)?"
    r"(?:/[^?#]*)?"
    r"(?:\?[^#]*)?"
    r"(?:#.*)?$",
    re.IGNORECASE,
)


def resolve_image_url(image_url: str) -> str:
    """
    Resolve an image URL if it belongs to a trusted domain.

    Parameters
    ----------
    image_url : str
        The URL of the image to resolve.

    Returns
    -------
    str
        The same URL if it is trusted and well‑formed.

    Raises
    ------
    ValueError
        If the URL is malformed or its domain is not in TRUSTED_DOMAINS.
    """
    # Basic sanity check
    if not isinstance(image_url, str):
        raise ValueError("image_url must be a string")

    # Ensure the URL matches the expected pattern
    match = URL_REGEX.match(image_url)
    if not match:
        raise ValueError(f"Malformed URL: {image_url}")

    # Parse the URL to extract components
    parsed = urlparse(image_url)

    # Normalize the host (lowercase, strip trailing dots)
    host = parsed.hostname.lower().rstrip(".")
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {host}")

    # Reconstruct the URL to ensure it is canonical
    canonical = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        parsed.query or "",
        ""   # fragment
    ))
    return canonical


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(resolve_image_url("https://i.imgur.com/example.png"))