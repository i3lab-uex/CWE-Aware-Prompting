import re
from urllib.parse import urlparse, unquote
import socket
import ipaddress

# --------------------------------------------------------------------------- #
# Whitelist of approved domains (add your own as needed)
APPROVED_DOMAINS = {
    # Fully qualified domain names
    "api.example.com",
    "services.partner.org",
    # Wildcards using regex patterns
    r"^api\.trusted-\w+\.com$",
}

# Regular expression for detecting private or local IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    (^10\.)|                           # 10.0.0.0/8
    (^172\.1[6-9]\.)|                 # 172.16.0.0/12
    (^172\.2[0-9]\.)|
    (^172\.3[0-1]\.)|
    (^192\.168\.)|                    # 192.168.0.0/16
    (^127\.0\.0\.1$)|                 # loopback
    (^169\.254\.)|                    # link-local
    (^0\.0\.0\.0$)|                   # unspecified
    (^255\.255\.255\.255$)            # broadcast
    """,
    re.VERBOSE,
)


def _is_private_ip(ip: str) -> bool:
    """
    Determine if the given IP address string is private or reserved.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_reserved
    except ValueError:
        # If parsing fails, fall back to regex check for typical patterns.
        return bool(PRIVATE_IP_REGEX.search(ip))


def _domain_is_approved(domain: str) -> bool:
    """
    Check if the domain matches one of the approved patterns.
    """
    for pattern in APPROVED_DOMAINS:
        if pattern.startswith(r"^"):
            # Treat as regex
            if re.match(pattern, domain):
                return True
        else:
            # Treat as literal string (case‑insensitive)
            if domain.lower() == pattern.lower():
                return True
    return False


def check_api_url(endpoint_url: str) -> str:
    """
    Validate that *endpoint_url* points to a trustworthy external API.

    Parameters
    ----------
    endpoint_url : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it is approved.

    Raises
    ------
    ValueError
        If the URL does not belong to an approved domain or if it targets
        internal network addresses.
    """
    # 1. Basic URL parsing
    parsed = urlparse(endpoint_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {endpoint_url!r}")

    # 2. Resolve hostname to IP(s)
    host = parsed.hostname
    if not host:
        raise ValueError(f"Missing hostname in URL: {endpoint_url!r}")

    # Unescape percent‑encoded hostnames (e.g., IPv6 in brackets)
    host = unquote(host)

    # Resolve to IP addresses (may return multiple)
    try:
        addr_info = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve host {host!r}: {exc}") from exc

    # 3. Ensure none of the resolved IPs are private/internal
    for _, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(
                f"URL resolves to a private or local IP ({ip}); "
                "potential SSRF detected."
            )

    # 4. Verify that the hostname is in the approved list
    if not _domain_is_approved(host):
        raise ValueError(
            f"Domain {host!r} is not in the approved list of external APIs."
        )

    # 5. Return the validated URL (unchanged)
    return endpoint_url