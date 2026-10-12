import re
from urllib.parse import urlparse

# List of trusted image hosting domains (case‑insensitive)
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "cdn.discordapp.com",
    "pbs.twimg.com",
    "images.unsplash.com",
    "upload.wikimedia.org",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

def _normalize_domain(domain: str) -> str:
    """
    Normalise the domain by stripping any leading 'www.' and converting to lowercase.
    """
    return re.sub(r"^www\.", "", domain.lower())

def fetch_image_url(url: str) -> str:
    """
    Resolve an image URL and verify that its domain belongs to a trusted list.

    Parameters
    ----------
    url : str
        The image URL to validate.

    Returns
    -------
    str
        The original URL if it is valid and trusted.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https or if the domain is not trusted.
    """
    # Parse the URL
    parsed = urlparse(url)
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"Unrecognized URL scheme: {parsed.scheme!r}")

    # Normalise and validate domain
    netloc = _normalize_domain(parsed.netloc.split(":")[0])  # ignore port if present
    if netloc not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain {netloc!r} is not trusted")

    # Reconstruct the URL to ensure consistent formatting
    verified_url = parsed.geturl()
    return verified_url

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         print(fetch_image_url("https://i.imgur.com/example.jpg"))
#     except ValueError as e:
#         print(e)