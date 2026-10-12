#!/usr/bin/env python3
"""
validate_picture_url

Validates that a given image URL comes from an approved list of trusted
image hosting providers and uses a supported scheme (http or https).

Raises:
    ValueError: If the URL's domain is not in the trusted list, or if
                the scheme is unsupported.
"""

from urllib.parse import urlparse
from typing import List


# List of approved domains (add or remove as needed)
_TRUSTED_DOMAINS: List[str] = [
    "imgur.com",
    "i.imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "flickr.com",
    "static.flickr.com",
    "upload.wikimedia.org",
]


def _is_trusted_domain(domain: str) -> bool:
    """
    Checks if the given domain or any of its parent domains is in the trusted list.
    E.g., 'i.imgur.com' matches 'imgur.com'.
    """
    # Normalize to lower case
    domain = domain.lower()
    for trusted in _TRUSTED_DOMAINS:
        if domain == trusted or domain.endswith("." + trusted):
            return True
    return False


def validate_picture_url(pic_url: str) -> str:
    """
    Validate that `pic_url` is a URL from a trusted image host and uses http/https.

    Parameters:
        pic_url (str): The URL to validate.

    Returns:
        str: The original `pic_url` if it is valid.

    Raises:
        ValueError: If the URL scheme is not http/https or the domain is untrusted.
    """
    if not isinstance(pic_url, str):
        raise ValueError("pic_url must be a string")

    parsed = urlparse(pic_url)

    # Check scheme
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure a network location is present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain)")

    # Validate domain
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.netloc}")

    # Basic path safety check – reject URLs that attempt directory traversal
    if ".." in parsed.path.split("/"):
        raise ValueError("URL path contains unsafe components")

    # Return the original URL unchanged
    return pic_url


# Example usage (uncomment to test)
if __name__ == "__main__":
    test_urls = [
        "https://i.imgur.com/example.jpg",
        "http://cdn.pixabay.com/photo/2020/01/01/12/34/example.jpg",
        "https://example.com/image.png",  # should raise
    ]

    for url in test_urls:
        try:
            print(f"Validating: {url}")
            valid = validate_picture_url(url)
            print("  -> Valid URL:", valid)
        except ValueError as exc:
            print("  -> Validation failed:", exc)