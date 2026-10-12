import re
from urllib.parse import urlparse, ParseResult
import ipaddress

# Regular expression to match common private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(10\.\d{1,3}\.\d{1,3}\.\d{1,3}|            # 10.0.0.0/8
    172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}|   # 172.16.0.0/12
    192\.168\.\d{1,3}\.\d{1,3}|                 # 192.168.0.0/16
    169\.254\.\d{1,3}\.\d{1,3}|                 # 169.254.0.0/16 (link-local)
    127\.\d{1,3}\.\d{1,3}\.\d{1,3}|             # 127.0.0.0/8 (loopback)
    ::1|                                      # IPv6 loopback
    fc00::/7|                                 # Unique local address (ULA)
    fd00::/8)                                  # Another ULA
    """,
    re.VERBOSE,
)

# List of allowed top‑level domains (example whitelist). Adjust as needed.
ALLOWED_TLDS = {"com", "org", "net", "io", "gov", "edu"}

def _is_private_ip(host: str) -> bool:
    """
    Return True if the host is a private IP address or a loopback.
    Handles both IPv4 and IPv6.
    """
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not an IP address, fall back to regex for older Python versions
        return bool(PRIVATE_IP_REGEX.match(host))

def _is_allowed_tld(netloc: str) -> bool:
    """
    Verify that the hostname ends with an allowed TLD.
    """
    if not netloc:
        return False
    # Strip port if present
    host = netloc.split(":")[0]
    parts = host.rsplit(".", 1)
    return len(parts) == 2 and parts[1].lower() in ALLOWED_TLDS

def check_api_endpoint(endpoint_url: str) -> str:
    """
    Validate that `endpoint_url` points to a secure, external API endpoint.

    The function performs the following checks:
        1. URL must use https scheme.
        2. Host must not resolve to a private IP address, loopback,
           or any internal network range.
        3. Host must have an allowed top‑level domain (whitelist).

    Parameters
    ----------
    endpoint_url : str
        The URL to validate.

    Returns
    -------
    str
        The original `endpoint_url` if it passes all checks.

    Raises
    ------
    ValueError
        If any of the validation checks fail.
    """
    if not isinstance(endpoint_url, str):
        raise ValueError("endpoint_url must be a string")

    parsed: ParseResult = urlparse(endpoint_url)

    # 1. Ensure HTTPS
    if parsed.scheme.lower() != "https":
        raise ValueError("Only https URLs are allowed")

    # 2. Host extraction
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # 3. Reject private IPs or loopback addresses
    if _is_private_ip(host):
        raise ValueError(f"Hostname {host!r} resolves to a private or loopback address")

    # 4. TLD whitelist
    if not _is_allowed_tld(parsed.netloc):
        raise ValueError(f"Hostname {host!r} does not end with an allowed TLD")

    # 5. Basic sanity: path must be present (optional, but common for APIs)
    if not parsed.path:
        raise ValueError("URL must contain a path component")

    return endpoint_url