import re
from urllib.parse import urlparse, ParseResult
import socket
import ipaddress

# Whitelist of allowed external domains (example)
ALLOWED_DOMAINS = {
    "api.example.com",
    "services.safe.org",
    # Add more approved domains here
}

# Regex for detecting localhost patterns
LOCALHOST_RE = re.compile(r"^(localhost|127\.0\.0\.1|::1)$", re.IGNORECASE)

def _is_private_ip(ip: str) -> bool:
    """
    Determine if an IP address is in a private, loopback,
    or reserved range.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_reserved
    except ValueError:
        # If not a valid IP, treat as non-private (shouldn't happen)
        return False

def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve a hostname to all associated IP addresses.
    """
    try:
        return [info[4][0] for info in socket.getaddrinfo(hostname, None)]
    except socket.gaierror:
        return []

def check_api_endpoint(endpoint_url: str) -> str:
    """
    Validate that the given URL points to a secure, external API endpoint.

    Parameters
    ----------
    endpoint_url : str
        The URL that needs to be verified.

    Returns
    -------
    str
        The validated URL if it is allowed.

    Raises
    ------
    ValueError
        If the URL targets an unapproved domain or any address within internal networks.
    """
    if not isinstance(endpoint_url, str):
        raise ValueError("URL must be a string")

    parsed: ParseResult = urlparse(endpoint_url)

    # Scheme must be http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Host must be present
    if not parsed.hostname:
        raise ValueError("URL does not contain a hostname")

    # Reject localhost patterns
    if LOCALHOST_RE.match(parsed.hostname):
        raise ValueError("Localhost addresses are disallowed")

    # Resolve hostname to IPs and check each
    ip_list = _resolve_hostname(parsed.hostname)
    if not ip_list:
        raise ValueError(f"Unable to resolve hostname: {parsed.hostname}")

    for ip in ip_list:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname {parsed.hostname} resolves to private IP: {ip}")

    # Check domain against whitelist
    if parsed.hostname.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain {parsed.hostname} is not approved")

    # If all checks pass, return the original URL
    return endpoint_url

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         safe_url = check_api_endpoint("https://api.example.com/data")
#         print(f"Allowed URL: {safe_url}")
#     except ValueError as e:
#         print(f"Validation failed: {e}")