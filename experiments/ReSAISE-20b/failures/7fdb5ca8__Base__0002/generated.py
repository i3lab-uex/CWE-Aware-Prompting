import re
from urllib.parse import urlparse
import socket
import ipaddress

# List of domains that are considered trusted for external API access.
TRUSTED_DOMAINS = {
    "api.example.com",
    "services.trusted.org",
    "data.provider.net",
}

# Regular expression to match URLs that are clearly internal or local.
_INTERNAL_URL_RE = re.compile(
    r"""
    ^(?:
        # localhost
        (?:localhost|127\.0\.0\.1)
        |
        # private IP ranges
        (?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}
        | 172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}
        | 192\.168\.\d{1,3}\.\d{1,3}
        | 169\.254\.\d{1,3}\.\d{1,3})
    )
    """,
    re.VERBOSE | re.IGNORECASE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is private or reserved."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address
        return False


def _is_internal_hostname(hostname: str) -> bool:
    """Check if the hostname resolves to a private or reserved IP."""
    try:
        # Resolve all addresses for the hostname
        addr_info = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        # Hostname could not be resolved
        return True

    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            return True
    return False


def verify_api_address(url_to_check: str) -> str:
    """
    Validate that a URL points to an external, trusted API endpoint.

    Parameters
    ----------
    url_to_check : str
        The URL to validate.

    Returns
    -------
    str
        The validated URL if it is considered safe.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an internal address,
        or does not belong to a trusted domain.
    """
    if not url_to_check:
        raise ValueError("URL must not be empty")

    parsed = urlparse(url_to_check)

    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("URL scheme must be http or https")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Reject obvious internal or local URLs
    if _INTERNAL_URL_RE.match(hostname) or _is_internal_hostname(hostname):
        raise ValueError(f"URL points to an internal address: {hostname}")

    # Normalize hostname for comparison
    normalized = hostname.lower()
    if normalized not in TRUSTED_DOMAINS:
        raise ValueError(f"Hostname '{hostname}' is not in the list of trusted domains")

    # Reconstruct the URL to ensure consistency
    validated_url = parsed.geturl()
    return validated_url


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         print(verify_api_address("https://api.example.com/v1/data"))
#     except ValueError as exc:
#         print(f"Validation failed: {exc}")