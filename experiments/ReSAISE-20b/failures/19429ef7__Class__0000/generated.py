import re
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------------- #
# Trusted image hosting domains. Add any additional providers here.
# The list can contain full domain names or subdomains.  A URL is accepted
# if its hostname ends with one of the entries (case‑insensitive).
_TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trustedprovider.org",
    "static.safe-host.net",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}


def _is_trusted_domain(hostname: str) -> bool:
    """
    Check whether *hostname* ends with one of the trusted domains.
    The check is case‑insensitive and guarantees that subdomains are
    allowed only if they explicitly match a trusted domain suffix.
    """
    hostname = hostname.lower()
    return any(hostname == domain or hostname.endswith("." + domain) for domain in _TRUSTED_DOMAINS)


def fetch_image_url(img_url: str) -> str:
    """
    Validate that *img_url* points to an image hosted on a trusted provider.

    Parameters
    ----------
    img_url : str
        The URL to validate and resolve.

    Returns
    -------
    str
        The validated, fully‑resolved URL.

    Raises
    ------
    ValueError
        If the URL has an unsupported scheme, is malformed,
        or points to an untrusted domain.
    """
    # Parse the URL and normalize components
    try:
        parsed = urlparse(img_url)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Malformed URL: {img_url}") from exc

    # Scheme must be http or https
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}'. Only http/https are allowed.")

    # Hostname must be present
    if not parsed.hostname:
        raise ValueError("URL does not contain a valid hostname.")

    # Domain must be in the trusted list
    if not _is_trusted_domain(parsed.hostname):
        raise ValueError(f"Untrusted domain '{parsed.hostname}'. Access denied.")

    # Reconstruct the URL to ensure it is fully resolved (e.g., remove fragment)
    cleaned = parsed._replace(fragment="", params="")
    return urlunparse(cleaned)

# --------------------------------------------------------------------------- #
# Example usage (for illustration only; remove or comment out in production)
if __name__ == "__main__":
    test_urls = [
        "https://images.example.com/path/to/image.jpg",
        "http://cdn.trustedprovider.org/abc.png?query=1#frag",
        "https://evil.com/hack.jpg",
    ]

    for url in test_urls:
        try:
            print(f"Validated URL: {fetch_image_url(url)}")
        except ValueError as e:
            print(f"Validation failed: {e}")