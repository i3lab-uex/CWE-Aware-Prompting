import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting providers (add more as needed)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "images.unsplash.com",
    "picsum.photos",
    "cdn.pixabay.com",
    "flickr.com",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}


def _is_trusted_domain(host: str) -> bool:
    """
    Check if the host ends with a trusted domain.
    Supports subdomains of trusted domains.
    """
    # Normalize host to lower case
    host = host.lower()
    for domain in _TRUSTED_DOMAINS:
        if host == domain or host.endswith("." + domain):
            return True
    return False


def validate_picture_url(pic_url: str) -> str:
    """
    Validate that a picture URL is from a trusted domain and uses an allowed scheme.
    
    Parameters
    ----------
    pic_url : str
        The input image URL to validate.

    Returns
    -------
    str
        The resolved, fully qualified URL if it is trusted.

    Raises
    ------
    ValueError
        If the domain is not in the trusted list or the scheme is unsupported.
    """
    if not isinstance(pic_url, str):
        raise ValueError("pic_url must be a string")

    parsed = urlparse(pic_url)

    # Ensure scheme is present and allowed
    if not parsed.scheme:
        raise ValueError("URL must include a scheme (http or https)")
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate host
    if not parsed.netloc:
        raise ValueError("URL must include a network location (domain)")
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not trusted")

    # Rebuild the URL to ensure it's canonical
    cleaned_url = urlunparse(parsed._replace(fragment=""))
    return cleaned_url


# Example usage (commented out to avoid accidental execution)
# if __name__ == "__main__":
#     try:
#         url = validate_picture_url("https://i.imgur.com/abcd1234.png")
#         print(f"Valid URL: {url}")
#     except ValueError as e:
#         print(f"Validation failed: {e}")