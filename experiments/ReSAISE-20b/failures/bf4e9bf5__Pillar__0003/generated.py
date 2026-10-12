#!/usr/bin/env python3
"""
Utility to validate and resolve image URLs against a whitelist of trusted domains.
"""

import re
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------------- #
# Trusted image hosting domains (usefully lowercase for case‑insensitive checks)
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trusted.com",
    "media.safe-host.org",
}

# Regular expression for a minimal but robust URL scheme validation
_URL_SCHEME_RE = re.compile(r"^(https?|ftp)://", re.IGNORECASE)


def _is_trusted_domain(netloc: str) -> bool:
    """
    Check whether the provided network location (domain + optional port)
    belongs to one of the trusted domains.
    """
    # Remove any trailing port number for comparison
    host = netloc.split(":")[0].lower()
    return host in TRUSTED_DOMAINS


def resolve_image_url(image_url: str) -> str:
    """
    Resolve an image URL after verifying that it belongs to a trusted domain.

    Parameters
    ----------
    image_url : str
        The image URL to be resolved.

    Returns
    -------
    str
        The normalized, fully‑qualified image URL.

    Raises
    ------
    ValueError
        If the URL is malformed or its domain is not in TRUSTED_DOMAINS.
    """
    if not isinstance(image_url, str):
        raise ValueError("image_url must be a string")

    # Ensure the URL has an allowed scheme
    if not _URL_SCHEME_RE.match(image_url):
        raise ValueError("image_url must start with http://, https://, or ftp://")

    parsed = urlparse(image_url)

    # Basic validation: must have a network location and path
    if not parsed.netloc or not parsed.path:
        raise ValueError("image_url must contain a valid domain and path")

    # Domain verification
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.netloc}")

    # Normalise the URL (e.g., remove duplicate slashes)
    cleaned_path = re.sub(r"/{2,}", "/", parsed.path)

    # Rebuild the URL with cleaned components
    resolved = urlunparse(
        (
            parsed.scheme,
            parsed.netloc.lower(),
            cleaned_path,
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return resolved


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test):
#
# if __name__ == "__main__":
#     try:
#         url = resolve_image_url("https://cdn.trusted.com/path//to/image.png")
#         print(f"Resolved URL: {url}")
#     except ValueError as exc:
#         print(f"Error: {exc}")