import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of fully‑qualified domains that are allowed to host images.
TRUSTED_DOMAINS = {
    "example.com",
    "images.trusted.org",
    "cdn.safeimage.net",
}

# Regex to detect an IPv4 or IPv6 address in a host part
IP_REGEX = re.compile(r"""
    ^(?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
      |
        # IPv6
        \[?[0-9a-fA-F:]+\]?
    )$
""", re.VERBOSE)


def _is_ip_address(host: str) -> bool:
    """Return True if the host string is an IP address."""
    return bool(IP_REGEX.match(host))


def resolve_image_url(image_url: str) -> str:
    """
    Resolve an image URL only if it belongs to a trusted domain.

    Parameters
    ----------
    image_url : str
        The URL to be resolved. Must be an absolute URL.

    Returns
    -------
    str
        The normalized, fully resolved URL.

    Raises
    ------
    ValueError
        If the URL is not absolute, or if its host is not in the trusted list,
        or if it resolves to a private/loopback IP address.
    """
    # Parse the URL
    parsed = urlparse(image_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute and contain a scheme and host")

    # Strip any port from the hostname for comparison
    host = parsed.hostname.lower()
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject URLs that are plain IP addresses
    if _is_ip_address(host):
        try:
            ip = ipaddress.ip_address(host.strip("[]"))
            if ip.is_private or ip.is_loopback:
                raise ValueError(f"Private or loopback IP address not allowed: {host}")
        except ValueError:
            # Not a valid IP – treat as hostname
            pass

    # Check against the list of trusted domains
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not trusted")

    # Normalize: enforce HTTPS scheme (optional – remove if you want to keep original)
    normalized = parsed._replace(scheme="https")
    return urlunparse(normalized)


# Example usage (commented out)
# if __name__ == "__main__":
#     try:
#         print(resolve_image_url("http://images.trusted.org/path/to/image.png"))
#     except ValueError as e:
#         print(f"Invalid URL: {e}")