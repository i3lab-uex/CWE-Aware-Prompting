import re
from urllib.parse import urlparse, urlunparse

# List of domains that are considered trusted for image hosting
TRUSTED_DOMAINS = {
    "imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "picsum.photos",
}

# Regular expression to detect IP addresses (IPv4 or IPv6)
_IP_RE = re.compile(
    r"""
    ^(?:
        # IPv4
        (?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})
        |
        # IPv6
        \[
            (?:(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}
            |(?:[A-Fa-f0-9]{1,4}:){6}:[A-Fa-f0-9]{1,4}
            |(?:[A-Fa-f0-9]{1,4}:){5}(?::[A-Fa-f0-9]{1,4}){1,2}
            |(?:[A-Fa-f0-9]{1,4}:){4}(?::[A-Fa-f0-9]{1,4}){1,3}
            |(?:[A-Fa-f0-9]{1,4}:){3}(?::[A-Fa-f0-9]{1,4}){1,4}
            |(?:[A-Fa-f0-9]{1,4}:){2}(?::[A-Fa-f0-9]{1,4}){1,5}
            |(?:[A-Fa-f0-9]{1,4}:)(?::[A-Fa-f0-9]{1,4}){1,6}
            |(?::(?:[A-Fa-f0-9]{1,4}:){0,7}[A-Fa-f0-9]{1,4})
            |(?:[A-Fa-f0-9]{1,4}:){7}:
        )
        \]
    )$
    """,
    re.VERBOSE,
)


def _is_ip_address(host: str) -> bool:
    """Return True if host is an IP address (IPv4 or IPv6)."""
    return bool(_IP_RE.match(host))


def _is_trusted_domain(netloc: str) -> bool:
    """
    Check if the netloc ends with one of the trusted domains.
    Subdomains are allowed as long as the root domain is trusted.
    """
    host = netloc.split(":")[0]  # strip port if present
    if _is_ip_address(host):
        return False

    for domain in TRUSTED_DOMAINS:
        if host == domain or host.endswith("." + domain):
            return True
    return False


def verify_image_url(img_url: str) -> str:
    """
    Verify that the supplied image URL belongs to a trusted domain
    and has an allowed scheme.

    Parameters
    ----------
    img_url : str
        The URL of the image to validate.

    Returns
    -------
    str
        The original URL if it passes validation.

    Raises
    ------
    ValueError
        If the scheme is not http/https, or if the domain is not trusted.
    """
    parsed = urlparse(img_url)

    # Ensure scheme is http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Reject URLs that resolve to an IP address
    if _is_ip_address(parsed.hostname or ""):
        raise ValueError("IP addresses are not allowed in image URLs")

    # Validate domain
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Domain not trusted: {parsed.netloc}")

    # Return the normalized URL (preserve original components)
    return urlunparse(parsed)


# Example usage
if __name__ == "__main__":
    test_urls = [
        "https://i.imgur.com/abc123.jpg",
        "http://cdn.pixabay.com/photo/2021/01/01/00/00/sample.jpg",
        "https://malicious.com/evil.png",
        "ftp://imgur.com/abc.jpg",
    ]

    for url in test_urls:
        try:
            print(f"Verified: {verify_image_url(url)}")
        except ValueError as e:
            print(f"Rejected: {url} -> {e}")