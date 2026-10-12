import re
from urllib.parse import urlparse, urlunparse

# List of fully-qualified domain names that are considered trusted image hosts.
TRUSTED_DOMAINS = {
    "imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "i.redd.it",
    "avatars.githubusercontent.com",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def _is_trusted_domain(netloc: str) -> bool:
    """
    Check if the given network location matches any of the trusted domains.
    Subdomains are considered acceptable only if they match a trusted domain
    exactly or end with the trusted domain prefixed by a dot.
    """
    # Remove potential port
    host = netloc.split(":")[0].lower()
    for domain in TRUSTED_DOMAINS:
        if host == domain or host.endswith("." + domain):
            return True
    return False


def validate_image_url(img_url: str) -> str:
    """
    Validate that the supplied image URL points to a trusted host
    and uses an allowed scheme (http or https).

    Parameters:
        img_url (str): The image URL to validate.

    Returns:
        str: The normalized, validated URL.

    Raises:
        ValueError: If the scheme is unsupported or the host
                    is not in the trusted list.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    parsed = urlparse(img_url)

    # Ensure scheme is present and allowed
    if not parsed.scheme or parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Validate host
    if not parsed.netloc or not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted host: {parsed.netloc!r}")

    # Reconstruct the URL to ensure consistent formatting
    normalized = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc,
        parsed.path,
        parsed.params,
        parsed.query,
        parsed.fragment
    ))

    return normalized