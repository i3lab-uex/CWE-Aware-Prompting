import re
from urllib.parse import urlparse
import socket
import ipaddress

# --------------------------------------------------------------------------- #
# Approved external domains.  Add any domain that is trusted to host APIs.
# --------------------------------------------------------------------------- #
APPROVED_DOMAINS = {
    "api.example.com",
    "services.trusted.org",
    "data.partner.net",
}

# --------------------------------------------------------------------------- #
# Regular expression to detect potential DNS rebinding attacks (e.g. 
# "http://localhost:8000") – only allow standard hostname patterns.
# --------------------------------------------------------------------------- #
HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)"
    r"(?:\.[A-Za-z0-9-]{1,63})*$"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or loopback."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback
    except ValueError:
        # Not a valid IP address (e.g., an IPv6 literal may be handled here)
        return False

def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve a hostname to its IPv4/IPv6 addresses."""
    try:
        _, _, ips = socket.gethostbyname_ex(hostname)
        return ips
    except socket.gaierror:
        raise ValueError(f"Unable to resolve hostname: {hostname}")

def validate_service_url(service_url: str) -> str:
    """
    Validate that a given URL points to an approved external API and does
    not target internal or private network addresses.

    Parameters:
        service_url (str): The URL to validate.

    Returns:
        str: The validated URL if it passes all checks.

    Raises:
        ValueError: If the URL is malformed, targets a disallowed domain,
                    or resolves to an internal/private IP address.
    """
    if not isinstance(service_url, str):
        raise ValueError("service_url must be a string")

    parsed = urlparse(service_url)

    # 1. Ensure we have a scheme and network location
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    # 2. Normalize the hostname (strip port if present)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("Unable to extract hostname")

    # 3. Validate the hostname format
    if not HOSTNAME_RE.match(hostname):
        raise ValueError(f"Invalid hostname: {hostname}")

    # 4. Check against approved domains
    if hostname not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not approved")

    # 5. Resolve the hostname to IP addresses and check for private IPs
    ips = _resolve_hostname(hostname)
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(
                f"Hostname '{hostname}' resolves to a private IP address ({ip})"
            )

    # 6. Reconstruct the URL (ensuring no query or fragment that could be
    #    misused by an attacker) – optionally you can preserve them.
    safe_url = parsed._replace(fragment="", query="").geturl()

    return safe_url

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test):
#
# try:
#     validated = validate_service_url("https://api.example.com/v1/resource")
#     print(f"Validated URL: {validated}")
# except ValueError as exc:
#     print(f"Validation failed: {exc}")