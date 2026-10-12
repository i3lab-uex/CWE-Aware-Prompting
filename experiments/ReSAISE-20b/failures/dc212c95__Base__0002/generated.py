import re
import socket
from urllib.parse import urlparse, ParseResult
import ipaddress

# List of approved public API domains (example)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.mycompany.org",
    "hooks.another-domain.net",
}

# Regular expression to reject obvious private IP addresses in the host part
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(                     # start of string
        10\.              # 10.x.x.x
      | 172\.(1[6-9]|2\d|3[0-1])\.   # 172.16.x.x - 172.31.x.x
      | 192\.168\.        # 192.168.x.x
      | 127\..*           # localhost loopback
      | 169\.254\.        # link-local
      | ::1               # IPv6 loopback
    )$
    """,
    re.VERBOSE,
)


def _is_private_host(host: str) -> bool:
    """
    Return True if the host resolves to a private IP address or is an explicit
    private IP literal.
    """
    # Directly check if host looks like a private IP
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not an IP literal, resolve DNS
        try:
            resolved_ips = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
        except socket.gaierror:
            # Cannot resolve host – treat as invalid
            return True

        for _, _, _, _, sockaddr in resolved_ips:
            ip_str = sockaddr[0]
            ip_obj = ipaddress.ip_address(ip_str)
            if ip_obj.is_private or ip_obj.is_loopback:
                return True
        return False


def validate_webhook_url(webhook_endpoint: str) -> str:
    """
    Validate a webhook URL supplied by an external service.

    Parameters
    ----------
    webhook_endpoint : str
        The raw URL string received from the external service.

    Returns
    -------
    str
        A validated, fully-qualified URL that can safely be used for an internal API request.

    Raises
    ------
    ValueError
        If the URL is malformed, points to a disallowed domain, or resolves to a private/internal network.
    """
    if not webhook_endpoint:
        raise ValueError("Empty URL provided")

    parsed: ParseResult = urlparse(webhook_endpoint)

    # Ensure scheme is http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure hostname exists
    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    # Reject obvious private IP literals
    if PRIVATE_IP_REGEX.match(parsed.hostname):
        raise ValueError("URL points to a private IP address")

    # Resolve hostname and check for private addresses
    if _is_private_host(parsed.hostname):
        raise ValueError("URL resolves to a private or internal IP address")

    # Normalize domain: strip port for comparison
    hostname_lower = parsed.hostname.lower()

    if hostname_lower not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{hostname_lower}' is not in the list of approved domains")

    # Reconstruct URL with normalized components
    cleaned = parsed._replace(
        path=parsed.path or "/",
        params="",
        query="",
        fragment=""
    )
    return cleaned.geturl()