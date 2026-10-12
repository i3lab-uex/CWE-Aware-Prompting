import re
import socket
from urllib.parse import urlparse, urlunparse

# List of domains that are considered trusted for external API calls.
TRUSTED_DOMAINS = {
    "api.example.com",
    "services.partner.org",
    "data.api.net",
}

# Regular expression to match IP addresses.
IP_RE = re.compile(r"^(?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})(?:\.(?!$)|$)){4}$")

# CIDR blocks for private IP ranges.
PRIVATE_CIDRS = [
    ("10.0.0.0", "10.255.255.255"),
    ("172.16.0.0", "172.31.255.255"),
    ("192.168.0.0", "192.168.255.255"),
    ("127.0.0.0", "127.255.255.255"),  # loopback
    ("169.254.0.0", "169.254.255.255"),  # link-local
]

def ip_to_int(ip: str) -> int:
    """Convert dotted‑quad IP string to integer."""
    parts = [int(p) for p in ip.split(".")]
    return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]

def is_private_ip(ip: str) -> bool:
    """Check if the IP address falls into a private or reserved range."""
    ip_int = ip_to_int(ip)
    for start, end in PRIVATE_CIDRS:
        if ip_to_int(start) <= ip_int <= ip_to_int(end):
            return True
    return False

def resolve_hostname(hostname: str) -> list[str]:
    """Return a list of IP addresses resolved from the hostname."""
    try:
        infos = socket.getaddrinfo(hostname, None, family=socket.AF_INET)
    except socket.gaierror:
        return []
    return list({info[4][0] for info in infos})  # unique IPs

def check_api_link(api_link: str) -> str:
    """
    Validate an API URL ensuring it points to a trusted domain and does not
    resolve to private or internal IP addresses.

    Parameters
    ----------
    api_link : str
        The URL to validate.

    Returns
    -------
    str
        The validated URL unchanged if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, not HTTPS/HTTP, points to an untrusted domain,
        or resolves to a private IP address.
    """
    # Basic syntax validation
    parsed = urlparse(api_link)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL scheme must be http or https")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (hostname)")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Reject URLs that are already IP addresses
    if IP_RE.match(hostname):
        ip = hostname
        if is_private_ip(ip):
            raise ValueError(f"IP address {ip} is private or reserved")
    else:
        # Resolve hostname and check each IP
        ips = resolve_hostname(hostname)
        if not ips:
            raise ValueError(f"Unable to resolve hostname: {hostname}")
        for ip in ips:
            if is_private_ip(ip):
                raise ValueError(f"Hostname {hostname} resolves to private IP {ip}")

    # Ensure the hostname is within the trusted domains
    if hostname.lower() not in TRUSTED_DOMAINS:
        raise ValueError(f"Hostname {hostname} is not a trusted domain")

    # Reconstruct the URL to canonical form
    validated = urlunparse(parsed._replace(scheme=parsed.scheme.lower()))
    return validated

# Example usage (commented out for library code)
# if __name__ == "__main__":
#     try:
#         print(check_api_link("https://api.example.com/v1/data"))
#     except ValueError as e:
#         print(f"Validation failed: {e}")