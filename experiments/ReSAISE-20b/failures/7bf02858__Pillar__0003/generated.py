import re
import socket
from urllib.parse import urlparse, ParseResult

# ------------------------------------------------------------------
# Configuration – approved domains and scheme whitelist
# ------------------------------------------------------------------
APPROVED_DOMAINS = {
    "api.example.com",
    "service.internal.company",
    "internal.api.local",
}

SCHEMES = {"http", "https"}

# ------------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------------
def _is_private_ip(ip: str) -> bool:
    """
    Return True if the IP address is in a private or reserved range.
    Uses simple regex checks for IPv4; IPv6 handling omitted for brevity.
    """
    private_patterns = [
        r"^10\.",          # 10.0.0.0/8
        r"^172\.(1[6-9]|2\d|3[0-1])\.",  # 172.16.0.0/12
        r"^192\.168\.",    # 192.168.0.0/16
        r"^127\.":          # localhost loopback
    ]
    return any(re.match(pat, ip) for pat in private_patterns)


def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve the hostname to a list of IP addresses.
    Raises socket.gaierror if resolution fails.
    """
    return [addr[4][0] for addr in socket.getaddrinfo(hostname, None)]


# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def process_hook(hook_url: str) -> str:
    """
    Validate a webhook URL and return it if it points to an approved
    public-facing API endpoint.

    Parameters:
        hook_url (str): The URL received from an external service.

    Returns:
        str: A validated and sanitized URL string.

    Raises:
        ValueError: If the URL is malformed, uses an unsupported scheme,
                    points to a non-approved domain, or resolves to
                    an internal/private IP address.
    """
    # Parse the URL
    parsed: ParseResult = urlparse(hook_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL: missing scheme or network location")

    # Scheme check
    if parsed.scheme.lower() not in SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Domain whitelist check
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Normalize the domain (case-insensitive)
    hostname_lower = hostname.lower()
    if hostname_lower not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not approved")

    # Resolve hostname to IPs and ensure none are private
    try:
        ip_addresses = _resolve_hostname(hostname_lower)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed: {exc}") from exc

    for ip in ip_addresses:
        if _is_private_ip(ip):
            raise ValueError(f"URL resolves to private IP address {ip}")

    # Reconstruct a sanitized URL (re-encode path/query/fragment)
    safe_url = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=hostname_lower,
    ).geturl()

    return safe_url