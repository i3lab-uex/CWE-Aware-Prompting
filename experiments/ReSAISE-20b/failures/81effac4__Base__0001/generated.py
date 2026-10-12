import re
import socket
from urllib.parse import urlparse, urlunparse

# A minimal list of trusted domains. Extend as needed.
TRUSTED_DOMAINS = {
    "api.example.com",
    "data.provider.org",
    "services.somecorp.net",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    (^127\.)|                     # localhost
    (^10\.)|                      # Class A private
    (^172\.(1[6-9]|2[0-9]|3[01])\.|# Class B private
    (^192\.168\.)                 # Class C private
    """,
    re.VERBOSE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private or reserved range."""
    # IPv4 only for simplicity; IPv6 can be added similarly
    if PRIVATE_IP_REGEX.search(ip):
        return True

    # Explicit check for link-local and multicast addresses
    first_octet = int(ip.split(".")[0])
    if 224 <= first_octet <= 239:  # multicast
        return True

    return False


def _normalize_url(parsed: urlparse) -> str:
    """Return a normalized URL string."""
    scheme = parsed.scheme or "https"
    netloc = parsed.netloc.lower()
    path = parsed.path or "/"
    return urlunparse((scheme, netloc, path, "", "", ""))


def check_api_link(api_link: str) -> str:
    """
    Validate that the provided API URL points to a trusted external domain
    and does not resolve to an internal or private IP address.

    Parameters
    ----------
    api_link : str
        The API URL to validate.

    Returns
    -------
    str
        A normalized, validated URL suitable for external API calls.

    Raises
    ------
    ValueError
        If the URL is not HTTP(S), does not belong to a trusted domain,
        or resolves to an internal/private IP address.
    """
    if not isinstance(api_link, str):
        raise ValueError("API link must be a string")

    parsed = urlparse(api_link)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a hostname")

    # Enforce domain whitelist
    if hostname not in TRUSTED_DOMAINS:
        raise ValueError(f"Hostname '{hostname}' is not trusted")

    # Resolve the hostname to IP(s) and check each
    try:
        addr_info = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve hostname '{hostname}': {exc}") from exc

    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(
                f"Hostname '{hostname}' resolves to private IP address {ip}"
            )

    # All checks passed; return a normalized URL
    return _normalize_url(parsed)