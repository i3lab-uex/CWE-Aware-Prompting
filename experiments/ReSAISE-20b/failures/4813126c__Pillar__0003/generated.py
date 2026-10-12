import re
from urllib.parse import urlparse, ParseResult

# List of approved domains. Add or remove as needed.
_TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.example.org",
    "pics.safehost.net",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}

def _is_trusted_domain(host: str) -> bool:
    """
    Determine if the host part of a URL is in the list of trusted domains.
    Only exact matches are allowed; sub‑domains are not automatically accepted
    to avoid domain spoofing (CWE-664).
    """
    # Normalize by removing trailing dots and converting to lowercase
    host = host.rstrip(".").lower()
    return host in _TRUSTED_DOMAINS

def verify_image_url(img_url: str) -> str:
    """
    Validate that an image URL points to a trusted domain and uses a
    recognized scheme. The function does **not** perform any network I/O,
    but it guarantees that the returned URL is safe to embed or fetch.

    Parameters
    ----------
    img_url : str
        The URL of the image to validate.

    Returns
    -------
    str
        The original URL if it is considered safe.

    Raises
    ------
    ValueError
        If the URL's scheme is not http/https, or if its host does not match
        any trusted domain.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    parsed: ParseResult = urlparse(img_url)

    # Validate scheme
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP/HTTPS are allowed.")

    # Validate netloc (host:port)
    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a valid hostname")

    if not _is_trusted_domain(host):
        raise ValueError(f"Untrusted host '{host}'. Allowed hosts: {', '.join(_TRUSTED_DOMAINS)}")

    # Optional: Ensure the URL is absolute
    if not parsed.netloc:
        raise ValueError("URL must be absolute")

    # Return the original URL; no modifications are made
    return img_url

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         safe_url = verify_image_url("https://images.example.com/pic.jpg")
#         print(f"Verified URL: {safe_url}")
#     except ValueError as e:
#         print(f"URL verification failed: {e}")