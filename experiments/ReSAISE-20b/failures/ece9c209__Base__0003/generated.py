import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of allowed API domains (add your trusted domains here)
ALLOWED_DOMAINS = [
    r'^api\.trusted\.com$',
    r'^service\.example\.org$',
    # Add more regex patterns as needed
]

# Regular expression for allowed schemes
ALLOWED_SCHEMES = re.compile(r'^(https?)$', re.IGNORECASE)


def _is_allowed_domain(host: str) -> bool:
    """Check if the host matches any of the allowed domain patterns."""
    for pattern in ALLOWED_DOMAINS:
        if re.match(pattern, host, re.IGNORECASE):
            return True
    return False


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private or non‑public range."""
    try:
        addr = ipaddress.ip_address(ip)
        return not (addr.is_global and not addr.is_reserved)
    except ValueError:
        # Not a valid IP address
        return True


def _resolve_hostname(host: str) -> list[str]:
    """Resolve a hostname to all IPv4 and IPv6 addresses."""
    try:
        infos = socket.getaddrinfo(host, None)
        return [sockaddr[0] for _, _, _, _, sockaddr in infos]
    except socket.gaierror:
        return []


def validate_api_endpoint(api_url: str) -> str:
    """
    Validate that `api_url` points to an external trusted API endpoint.

    Parameters
    ----------
    api_url : str
        The URL to be validated.

    Returns
    -------
    str
        The original URL if it passes validation checks.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a disallowed domain, or resolves to a private
        internal address.
    """
    if not isinstance(api_url, str):
        raise ValueError("api_url must be a string")

    # Parse the URL
    parsed = urlparse(api_url)

    if not ALLOWED_SCHEMES.match(parsed.scheme):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http and https are allowed.")

    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    host = parsed.hostname
    if not host:
        raise ValueError("Could not extract hostname from URL")

    # Check that the hostname is an allowed domain
    if not _is_allowed_domain(host):
        raise ValueError(f"Hostname '{host}' is not in the list of allowed domains")

    # Resolve hostname to IP addresses
    ips = _resolve_hostname(host)
    if not ips:
        raise ValueError(f"Could not resolve hostname '{host}'")

    # Ensure all resolved IPs are public
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' for host '{host}' is not a public address")

    # Reconstruct the URL to ensure consistent formatting
    validated_url = urlunparse(parsed)
    return validated_url


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    try:
        url = "https://api.trusted.com/v1/data"
        print(validate_api_endpoint(url))
    except ValueError as exc:
        print(f"Validation failed: {exc}")