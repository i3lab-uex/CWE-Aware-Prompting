import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved API endpoints (hostnames or IPs)
APPROVED_HOSTS = {
    "api.example.com",
    "api.internal.company.local",  # internal but approved
    "192.168.1.100",
}

# Regular expression to detect private IP ranges quickly
PRIVATE_IP_RE = re.compile(
    r"""
    ^(?:
        10\.           # 10.0.0.0 – 10.255.255.255
      | 172\.(1[6-9]|2\d|3[0-1])\.   # 172.16.0.0 – 172.31.255.255
      | 192\.168\.   # 192.168.0.0 – 192.168.255.255
    )
    """,
    re.VERBOSE,
)

def _is_private_ip(host: str) -> bool:
    """
    Return True if host is a private IP address.
    """
    try:
        # Resolve numeric IPv4/IPv6
        ip = ipaddress.ip_address(host)
        return ip.is_private
    except ValueError:
        # Not an IP address, so cannot be private
        return False

def process_hook(hook_url: str) -> str:
    """
    Validate a webhook URL and ensure it points to an approved API endpoint.

    Parameters
    ----------
    hook_url : str
        The URL provided by the external service.

    Returns
    -------
    str
        A safely validated URL that references an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is outside the list of approved API endpoints or
        aims at an internal network location.
    """
    if not hook_url:
        raise ValueError("Empty URL")

    parsed = urlparse(hook_url)

    # Basic scheme check
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject private IP addresses that are not explicitly approved
    if _is_private_ip(host):
        if host not in APPROVED_HOSTS:
            raise ValueError(f"Private IP address {host} is not approved")

    # Reject private subdomains if the host is not in the whitelist
    if host not in APPROVED_HOSTS:
        # Check for subdomains of approved hosts (e.g., api.example.com.foo)
        if not any(host.endswith("." + approved) for approved in APPROVED_HOSTS):
            raise ValueError(f"Host {host} is not an approved API endpoint")

    # Ensure the URL does not contain unsafe path components (e.g., "..")
    if ".." in parsed.path:
        raise ValueError("URL path contains disallowed '..' component")

    # Reconstruct the URL to ensure normalisation
    safe_url = urlunparse(parsed._replace(fragment=""))
    return safe_url