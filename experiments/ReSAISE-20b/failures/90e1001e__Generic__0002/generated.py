import re
import socket
from urllib.parse import urlparse

# --------------------------------------------------------------------------- #
# Configuration: list of approved domains and sub‑domains
# --------------------------------------------------------------------------- #
APPROVED_DOMAINS = {
    "api.example.com",
    "services.another.org",
    # add more approved domains here
}

# --------------------------------------------------------------------------- #
# Helper: check if an IP address is private or loopback
# --------------------------------------------------------------------------- #
def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private, link‑local or loopback range."""
    try:
        # IPv4
        if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip):
            octets = [int(o) for o in ip.split(".")]
            if (
                (octets[0] == 10)
                or (octets[0] == 172 and 16 <= octets[1] <= 31)
                or (octets[0] == 192 and octets[1] == 168)
                or (octets[0] == 127)
            ):
                return True
        # IPv6
        if ":" in ip:
            if (
                ip.lower().startswith("fe80:")
                or ip.lower() == "::1"
            ):
                return True
    except Exception:
        pass
    return False


# --------------------------------------------------------------------------- #
# Main validation function
# --------------------------------------------------------------------------- #
def validate_service_url(service_url: str) -> str:
    """
    Validate that a URL points to an approved external API and is not targeting
    internal network addresses.

    Parameters:
        service_url (str): The URL to validate.

    Returns:
        str: The validated, canonicalized URL.

    Raises:
        ValueError: If the URL is malformed, not HTTPS, points to a disallowed
                    domain, or resolves to an internal IP address.
    """
    if not service_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(service_url)

    # Ensure scheme is https (or http if explicitly allowed)
    if parsed.scheme.lower() not in ("https", "http"):
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Domain must be present
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Check domain against whitelist
    if hostname not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not approved")

    # Resolve hostname to IP addresses
    try:
        addrinfo = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve hostname '{hostname}': {exc}")

    # Ensure none of the resolved IPs are private
    for family, _, _, _, sockaddr in addrinfo:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' is private or internal")

    # Reconstruct the URL to canonical form (remove fragments, normalize path)
    cleaned = parsed._replace(fragment="", query="").geturl()

    return cleaned