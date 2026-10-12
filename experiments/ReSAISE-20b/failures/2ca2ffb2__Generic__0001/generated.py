import urllib.parse

# List of trusted domains (exact matches). Use a wildcard entry like '*.example.com'
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "*.trustedhost.net",   # wildcard for subdomains
}

def _is_trusted_domain(domain: str) -> bool:
    """
    Check if the given domain is in the TRUSTED_DOMAINS set.
    Supports simple wildcard patterns of the form '*.example.com'.
    """
    for pattern in TRUSTED_DOMAINS:
        if pattern.startswith("*."):
            # wildcard match: any subdomain of the base domain
            base = pattern[2:]  # strip '*.'
            if domain == base or domain.endswith("." + base):
                return True
        else:
            if domain == pattern:
                return True
    return False

def fetch_image_url(url: str) -> str:
    """
    Validate that the provided image URL uses a recognized scheme (http/https)
    and its domain is in the list of trusted image hosting services.

    Parameters
    ----------
    url : str
        The URL of the image to resolve.

    Returns
    -------
    str
        The verified image URL if the domain is approved.

    Raises
    ------
    ValueError
        If the image URL doesn't belong to a trusted domain or if the scheme is unrecognized.
    """
    parsed = urllib.parse.urlparse(url)

    # Ensure we have a valid scheme
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unrecognized URL scheme: {parsed.scheme}")

    # Ensure we have a netloc (domain)
    if not parsed.netloc:
        raise ValueError("URL does not contain a valid domain")

    # Normalize the netloc (lowercase, strip port if present)
    host = parsed.hostname.lower() if parsed.hostname else ""
    if not _is_trusted_domain(host):
        raise ValueError(f"Domain '{host}' is not in the list of trusted image hosts")

    # Reconstruct the URL to ensure it is canonical (in case the original had uppercase letters)
    return urllib.parse.urlunparse(parsed._replace(netloc=parsed.netloc.lower()))

# Example usage (for testing purposes only)
if __name__ == "__main__":
    test_urls = [
        "https://i.imgur.com/abc123.jpg",
        "http://cdn.pixabay.com/photo/2020/01/01/00-00-00.jpg",
        "https://sub.trustedhost.net/image.png",
        "ftp://i.imgur.com/abc123.jpg",          # invalid scheme
        "https://malicious.com/image.png"         # untrusted domain
    ]

    for u in test_urls:
        try:
            print(f"Verified: {fetch_image_url(u)}")
        except ValueError as e:
            print(f"Rejected: {u} -> {e}")