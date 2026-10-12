import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of domains that are considered trusted API endpoints.
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.internal.company.com",
    "trusted.api.net",
}

# Regular expression to match private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    (^127\.0\.0\.1$)|
    (^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$)|
    (^172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}$)|
    (^192\.168\.\d{1,3}\.\d{1,3}$)|
    (^169\.254\.\d{1,3}\.\d{1,3}$)
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is a private address or loopback."""
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback
    except ValueError:
        # Not a valid IP address
        return False

def _is_allowed_domain(host: str) -> bool:
    """Check if the host is in the list of allowed domains."""
    # Normalize the host (lowercase, strip trailing dot)
    normalized = host.lower().rstrip(".")
    return any(
        normalized == allowed or normalized.endswith("." + allowed)
        for allowed in ALLOWED_DOMAINS
    )

def validate_api_endpoint(api_url: str) -> str:
    """
    Validate that `api_url` points to a trusted external API endpoint.

    Parameters
    ----------
    api_url : str
        The URL to validate.

    Returns
    -------
    str
        The validated, canonical URL.

    Raises
    ------
    ValueError
        If the URL is not part of an allowed domain or attempts to reach an internal network address.
    """
    if not api_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(api_url)

    # Ensure scheme is http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Resolve hostname to IP(s) and check for private addresses
    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a hostname")

    # Reject any IP addresses that are private or loopback
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", host) or re.match(r"^[0-9a-fA-F:]+$", host):
        if _is_private_ip(host):
            raise ValueError(f"URL resolves to a private IP: {host}")

    # Reject hostnames that are clearly internal (e.g., contain 'localhost' or '127.0.0.1')
    if host.lower() in {"localhost", "127.0.0.1"}:
        raise ValueError("URL points to a local host")

    # Ensure the hostname is in the list of allowed domains
    if not _is_allowed_domain(host):
        raise ValueError(f"Domain '{host}' is not in the list of allowed domains")

    # Reconstruct a canonical URL (strip fragments, normalize path)
    clean = parsed._replace(fragment="", query="")
    return urlunparse(clean)

# Example usage (for testing purposes only):
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/v1/resource",
        "http://10.0.0.5/api",          # Should raise ValueError
        "https://malicious.com/attack",
    ]
    for url in test_urls:
        try:
            print(f"Validated: {validate_api_endpoint(url)}")
        except ValueError as e:
            print(f"Invalid URL: {url} -> {e}")