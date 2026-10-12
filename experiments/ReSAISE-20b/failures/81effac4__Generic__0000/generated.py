import re
import socket
from urllib.parse import urlparse
import ipaddress

# List of domains considered trusted. Adjust as needed.
_TRUSTED_DOMAINS = {
    "api.trusted.com",
    "service.example.org",
    "public-api.company.net",
}

# Regular expression to quickly reject obvious localhost or private IP patterns
_PRIVATE_HOSTNAME_RE = re.compile(
    r"^(?:localhost|127\.\d+\.\d+\.\d+|0\.0\.0\.0)$", re.IGNORECASE
)

# Private IP ranges according to RFC 1918 and loopback
_PRIVATE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),  # loopback
    ipaddress.ip_network("::1/128"),     # IPv6 loopback
]


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private or loopback range."""
    try:
        addr = ipaddress.ip_address(ip)
        return any(addr in net for net in _PRIVATE_IP_RANGES)
    except ValueError:
        # Not a valid IP address
        return False


def _resolve_host_to_ips(hostname: str):
    """Return a set of IP addresses resolved from the hostname."""
    try:
        # getaddrinfo returns tuples: (family, type, proto, canonname, sockaddr)
        infos = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed for {hostname!r}: {exc}") from exc

    ips = set()
    for info in infos:
        sockaddr = info[4]
        # IPv6 addresses are tuples like (address, port, flowinfo, scopeid)
        ip = sockaddr[0]
        ips.add(ip)
    return ips


def check_api_link(api_link: str) -> str:
    """
    Validate that `api_link` points to an external, trusted API.

    Parameters
    ----------
    api_link : str
        The URL to validate.

    Returns
    -------
    str
        The validated URL (unchanged).

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a non‑trusted domain, or resolves to a private IP.
    """
    if not isinstance(api_link, str):
        raise ValueError("api_link must be a string")

    parsed = urlparse(api_link)

    # Ensure scheme is http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme {parsed.scheme!r}")

    if not parsed.netloc:
        raise ValueError("URL must include a hostname")

    # Reject obvious localhost or private hostnames
    if _PRIVATE_HOSTNAME_RE.match(parsed.hostname):
        raise ValueError("URL points to localhost or a private hostname")

    # Check if the domain is in our trusted list
    host_lower = parsed.hostname.lower()
    if host_lower not in _TRUSTED_DOMAINS:
        raise ValueError(f"Hostname {host_lower!r} is not in the trusted domains list")

    # Resolve hostname to IPs and ensure none are private
    resolved_ips = _resolve_host_to_ips(host_lower)
    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(
                f"Hostname {host_lower!r} resolves to private IP address {ip}"
            )

    # If we reach here, the URL is considered safe
    return api_link