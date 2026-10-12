import re
import socket
from urllib.parse import urlparse, urlunparse

# List of domains that are explicitly allowed for API calls.
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.mycompany.io",
    # Add more approved domains here.
}

# Regular expression that matches RFC1918 private IP ranges and
# other non‑public address spaces.
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (?:                      # start of group for the whole pattern
        10\.                #   10.0.0.0 – 10.255.255.255
        (?:\d{1,3}\.){2}
        \d{1,3}
    |
        172\.              #   172.16.0.0 – 172.31.255.255
        (?:1[6-9]|2\d|3[0-1])\.
        (?:\d{1,3}\.)
        \d{1,3}
    |
        192\.168\.         #   192.168.0.0 – 192.168.255.255
        (?:\d{1,3}\.)
        \d{1,3}
    |
        127\.              #   Loopback
        (?:\d{1,3}\.){2}
        \d{1,3}
    |
        169\.254\.         #   Link‑local
        (?:\d{1,3}\.)
        \d{1,3}
    |
        0\.               #   "0.0.0.0" or unspecified
        (?:\d{1,3}\.){2}
        \d{1,3}
    |
        255\.            #   Broadcast
        (?:\d{1,3}\.){2}
        \d{1,3}
    )
    $
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is private or otherwise
    non‑public according to RFC1918 and related specifications."""
    # Fast regex check first
    if PRIVATE_IP_REGEX.match(ip):
        return True
    try:
        # Resolve to integer and check for private ranges programmatically.
        packed = socket.inet_aton(ip)
    except OSError:
        # Not a valid IPv4 address.
        return False
    ip_int = int.from_bytes(packed, "big")
    # 10.0.0.0/8
    if ip_int >> 24 == 10:
        return True
    # 172.16.0.0/12
    if (ip_int >> 20) == 172 << 4:
        return True
    # 192.168.0.0/16
    if ip_int >> 16 == (192 << 8) + 168:
        return True
    # Loopback, link‑local, broadcast, etc.
    if (ip_int >> 24) in {127, 169, 255}:
        return True
    return False

def _is_allowed_domain(domain: str) -> bool:
    """Check if the domain is in the approved list."""
    return domain.lower() in ALLOWED_DOMAINS

def check_api_endpoint(endpoint_url: str) -> str:
    """
    Validate that *endpoint_url* points to a public, approved external API
    endpoint. The function performs the following checks:

    1. The URL must use http or https.
    2. The hostname must be in the ALLOWED_DOMAINS set.
    3. The resolved IP address of the hostname must not belong to
       private, loopback, link‑local or other non‑public ranges.

    If all checks pass the function returns a normalized URL (scheme,
    hostname, port, path).  Otherwise it raises ValueError.
    """
    if not isinstance(endpoint_url, str):
        raise TypeError("endpoint_url must be a string")

    parsed = urlparse(endpoint_url)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # 1. Domain whitelist
    if not _is_allowed_domain(parsed.hostname):
        raise ValueError(f"Domain '{parsed.hostname}' is not approved")

    # 2. Resolve hostname to IP(s)
    try:
        addr_info = socket.getaddrinfo(parsed.hostname, parsed.port or 0, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{parsed.hostname}': {exc}") from exc

    # 3. Ensure none of the IPs are private
    for family, _, _, _, sockaddr in addr_info:
        if family == socket.AF_INET:          # IPv4
            ip = sockaddr[0]
        elif family == socket.AF_INET6:       # IPv6
            ip = sockaddr[0]
        else:
            continue  # Skip unknown families

        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' for host '{parsed.hostname}' is private or non‑public")

    # Normalise URL: remove default port if present, rebuild path
    netloc = parsed.hostname
    if parsed.port and ((parsed.scheme == "http" and parsed.port != 80) or
                        (parsed.scheme == "https" and parsed.port != 443)):
        netloc += f":{parsed.port}"
    normalized = urlunparse((parsed.scheme, netloc, parsed.path or "", "", "", ""))

    return normalized