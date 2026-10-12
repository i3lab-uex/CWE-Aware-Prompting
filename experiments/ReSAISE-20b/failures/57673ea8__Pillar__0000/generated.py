import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# --------------------------------------------------------------------------- #
# Trusted provider list – keep only external, well‑known RSS sources
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.reuters.com",
}

# --------------------------------------------------------------------------- #
def _is_internal_ip(ip: str) -> bool:
    """
    Return True if the IP address belongs to a private or reserved range.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_reserved
    except ValueError:
        # Not a valid IP address
        return False


def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve a hostname to all IPv4 addresses. Raises socket.gaierror on failure.
    """
    return list(set(ip[4][0] for ip in socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)))


def validate_feed_url(url: str) -> str:
    """
    Validate that the given RSS feed URL originates from a trusted provider
    and does not resolve to an internal IP address.

    Parameters:
        url (str): The RSS feed URL to validate.

    Returns:
        str: The original URL if it is trusted and safe.

    Raises:
        ValueError: If the URL is malformed, not HTTPS, from an untrusted
                    provider, or resolves to an internal IP address.
    """
    if not isinstance(url, str) or not url:
        raise ValueError("URL must be a non-empty string")

    # Basic URL parsing
    parsed = urlparse(url)
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError("URL must use HTTP or HTTPS scheme")

    if not parsed.netloc:
        raise ValueError("Malformed URL: missing network location")

    hostname = parsed.hostname.lower()

    # Ensure the provider is in the trusted list
    if hostname not in TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted provider: {hostname}")

    # Resolve the hostname to IPs and check for internal addresses
    try:
        ip_list = _resolve_hostname(hostname)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname {hostname}") from exc

    for ip in ip_list:
        if _is_internal_ip(ip):
            raise ValueError(f"Hostname {hostname} resolves to internal IP: {ip}")

    # Re‑assemble the URL (to normalise it)
    cleaned = urlunparse(parsed._replace(netloc=parsed.netloc.lower()))
    return cleaned


# --------------------------------------------------------------------------- #
# Example usage (commented out – remove for production)
# if __name__ == "__main__":
#     try:
#         safe_url = validate_feed_url("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
#         print(f"Validated URL: {safe_url}")
#     except ValueError as e:
#         print(f"Validation failed: {e}")