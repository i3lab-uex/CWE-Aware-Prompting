import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (add or remove as needed)
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trustedhost.org",
    "pics.safe-site.net",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

# Regex to validate a basic URL format
_URL_REGEX = re.compile(
    r"^(?P<scheme>https?|ftp)://"
    r"(?P<netloc>[a-zA-Z0-9.-]+)"
    r"(?:\:[0-9]{1,5})?"
    r"(?P<path>/[^\s]*)?$",
    re.IGNORECASE,
)


def fetch_image_url(img_url: str) -> str:
    """
    Validate and return a fully qualified image URL.

    Parameters
    ----------
    img_url : str
        The user supplied image URL.

    Returns
    -------
    str
        The validated, fully resolved image URL.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        or points to an untrusted domain.
    """
    if not isinstance(img_url, str):
        raise ValueError("Image URL must be a string")

    # Basic sanity check with regex
    match = _URL_REGEX.match(img_url)
    if not match:
        raise ValueError("Malformed URL")

    parsed = urlparse(img_url)

    # Ensure scheme is allowed
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalize domain to lower case for comparison
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Verify the domain is in the whitelist
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {host}")

    # Reconstruct the URL to ensure consistency
    cleaned_url = urlunparse(
        (
            parsed.scheme.lower(),
            host,
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            parsed.fragment or "",
        )
    )

    return cleaned_url