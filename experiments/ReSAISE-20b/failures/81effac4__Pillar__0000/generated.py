import re
import socket
from urllib.parse import urlparse, urlunparse

# ------------------------------------------------------------------
# Trusted domain list – replace with your own trusted hosts
TRUSTED_DOMAINS = {
    "api.trusted.com",
    "services.example.org",
    "data.partner.net",
}

# Regular expression for private IPv4/IPv6 address blocks
PRIVATE_IP_REGEX = re.compile(
    r"""
    (^127\.|^10\.|^192\.168\.|^172\.(1[6-9]|2\d|3[0-1])\.|
    ^::1$|^fe80:|^fc00:|^fd00:)
    """,
    re.VERBOSE,
)

# ------------------------------------------------------------------
def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or loopback."""
    # IPv4
    try:
        octets = [int(o) for o in ip.split(".")]
        if len(octets) == 4:
            if octets[0] == 127:                # loopback
                return True
            if octets[0] == 10:
                return True
            if octets[0] == 192 and octets[1] == 168:
                return True
            if octets[0] == 172 and 16 <= octets[1] <= 31:
                return True
    except ValueError:
        pass

    # IPv6 (basic check for loopback and link-local)
    if ip.lower() in ("::1", "0:0:0:0:0:0:0:1"):
        return True
    if ip.lower().startswith("fe80") or ip.lower().startswith("fc00") or ip.lower().startswith("fd00"):
        return True

    return False


def _resolve_host_to_ip(host: str) -> set[str]:
    """Return a set of IP addresses resolved for the given host."""
    try:
        addr_info = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return set()
    ips = {info[4][0] for info in addr_info}
    return ips


def _validate_trusted_domain(host: str) -> bool:
    """Check if the host is in the list of trusted domains or a sub‑domain."""
    # Exact match
    if host.lower() in TRUSTED_DOMAINS:
        return True
    # Sub‑domain check (e.g., api.trusted.com)
    for domain in TRUSTED_DOMAINS:
        if host.lower().endswith("." + domain):
            return True
    return False


def check_api_link(api_link: str) -> str:
    """
    Validate that an API URL points to an external, trusted endpoint.

    Parameters
    ----------
    api_link : str
        The URL to validate.

    Returns
    -------
    str
        Normalised, validated URL suitable for external API use.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an internal or private network,
        or does not belong to a trusted domain.
    """
    if not api_link:
        raise ValueError("Empty URL provided")

    # Parse and normalise the URL
    parsed = urlparse(api_link.strip())
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Resolve the hostname to IP addresses
    ips = _resolve_host_to_ip(host)
    if not ips:
        raise ValueError(f"Could not resolve hostname: {host}")

    # Ensure none of the resolved IPs are private/internal
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"URL resolves to private IP address: {ip}")

    # Verify that the hostname is in the trusted domain list
    if not _validate_trusted_domain(host):
        raise ValueError(f"Hostname '{host}' is not in the list of trusted domains")

    # Rebuild a canonical URL (ensuring no user‑info or fragments)
    safe_netloc = host
    if parsed.port:
        safe_netloc += f":{parsed.port}"
    normalized = urlunparse(
        (
            parsed.scheme,
            safe_netloc,
            parsed.path or "/",
            "",  # params
            parsed.query,
            "",  # fragment
        )
    )

    return normalized

# ------------------------------------------------------------------
# Example usage (remove or comment out in production)
if __name__ == "__main__":
    test_urls = [
        "https://api.trusted.com/v1/data",
        "http://localhost:8000/api",           # should fail
        "https://192.168.1.10/service",       # should fail
        "https://api.untrusted.com/info",     # should fail
    ]

    for url in test_urls:
        try:
            print(f"Validating: {url}")
            print(" ->", check_api_link(url))
        except ValueError as e:
            print(f"  Error: {e}")