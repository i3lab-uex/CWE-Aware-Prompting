import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (case‑insensitive)
_TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "flickr.com",
    "upload.wikimedia.org",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}


def _is_trusted_domain(netloc: str) -> bool:
    """
    Check if the hostname is in the trusted domain list.
    Subdomains are considered valid only if they match exactly
    one of the entries in _TRUSTED_DOMAINS.
    """
    host = netloc.lower()
    return any(host == domain or host.endswith("." + domain) for domain in _TRUSTED_DOMAINS)


def get_image_link(link_image: str) -> str:
    """
    Validate and return a complete image URL.

    Parameters
    ----------
    link_image : str
        The user supplied image URL to validate and resolve.

    Returns
    -------
    str
        The fully resolved, validated image URL.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, contains a malicious path,
        or points to an untrusted domain.
    """
    if not isinstance(link_image, str):
        raise ValueError("link_image must be a string")

    # Parse the URL
    parsed = urlparse(link_image)

    # Scheme must be http or https
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure hostname exists
    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    # Validate domain
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.hostname}")

    # Reject URLs with suspicious path components (e.g., back‑references)
    if re.search(r"\.\./", parsed.path):
        raise ValueError("URL path contains invalid sequences")

    # Re‑build the URL to ensure it is canonical
    safe_parsed = parsed._replace(fragment="", params="")
    return urlunparse(safe_parsed)


# Example usage (for demonstration only, remove or comment out in production)
if __name__ == "__main__":
    test_urls = [
        "https://i.imgur.com/example.png",
        "http://cdn.pixabay.com/photo/2020/01/01/00/00/example.jpg",
        "https://malicious.com/bad.png",
    ]
    for url in test_urls:
        try:
            print(f"Validated: {get_image_link(url)}")
        except ValueError as e:
            print(f"Rejected: {url} -> {e}")