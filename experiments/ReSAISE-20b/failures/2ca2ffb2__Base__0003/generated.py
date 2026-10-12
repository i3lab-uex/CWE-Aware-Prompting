import re
from urllib.parse import urlparse, urlunparse

# A minimal list of trusted image hosting domains.
_TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "picsum.photos",
    "cdn.pixabay.com",
    "upload.wikimedia.org",
}

# Allowed URL schemes.
_ALLOWED_SCHEMES = {"http", "https"}

def fetch_image_url(url: str) -> str:
    """
    Validate that an image URL belongs to a trusted domain and uses an allowed scheme.

    Parameters
    ----------
    url : str
        The image URL to validate and return.

    Returns
    -------
    str
        The original URL if it passes validation checks.

    Raises
    ------
    ValueError
        If the URL does not use an allowed scheme, or if its domain is not trusted.
    """
    # Basic sanity check: must be a string
    if not isinstance(url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(url)

    # Ensure scheme is present and allowed
    if not parsed.scheme or parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Reject URLs with empty netloc (e.g., relative paths)
    if not parsed.netloc:
        raise ValueError("URL must contain a domain name")

    # Normalize the host (lowercase)
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Reject IP addresses (to mitigate SSRF)
    ip_pattern = re.compile(r"""
        ^
        (?:
            # IPv4
            (?:25[0-5]|2[0-4]\d|1?\d{1,2})\.
            (?:25[0-5]|2[0-4]\d|1?\d{1,2})\.
            (?:25[0-5]|2[0-4]\d|1?\d{1,2})\.
            (?:25[0-5]|2[0-4]\d|1?\d{1,2})
            |
            # IPv6
            \[
                (?:
                    [0-9a-fA-F]{1,4}
                    (?:\:[0-9a-fA-F]{1,4}){7}
                )
            \]
        )
        $
    """, re.VERBOSE)

    if ip_pattern.match(host):
        raise ValueError("IP addresses are not allowed for image URLs")

    # Check that the host ends with a trusted domain
    if not any(host == d or host.endswith("." + d) for d in _TRUSTED_DOMAINS):
        raise ValueError(f"Domain {host!r} is not trusted")

    # Reconstruct the URL to ensure consistency
    safe_url = urlunparse(parsed._replace(scheme=parsed.scheme.lower(), hostname=host))
    return safe_url