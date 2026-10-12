import re
import socket
from urllib.parse import urlparse

# --------------------------------------------------------------------------- #
# Trusted domain configuration – adjust to your environment
# --------------------------------------------------------------------------- #

TRUSTED_DOMAINS = {
    "api.example.com",
    "service.another.org",
    # Add any other fully qualified domain names you consider safe
}

# Optional: allow sub‑domains of the trusted domains
ALLOW_SUBDOMAINS = True

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_internal_ip(ip: str) -> bool:
    """
    Return True if the given IP address is in a private, reserved or
    loopback range.
    """
    # IPv4 handling
    try:
        octets = [int(o) for o in ip.split(".")]
        if len(octets) == 4:
            # 10.0.0.0/8
            if octets[0] == 10:
                return True
            # 172.16.0.0/12
            if octets[0] == 172 and 16 <= octets[1] <= 31:
                return True
            # 192.168.0.0/16
            if octets[0] == 192 and octets[1] == 168:
                return True
            # Loopback
            if octets[0] == 127:
                return True
    except ValueError:
        pass

    # IPv6 handling – check for ::1 (loopback) or fc00::/7 (unique local)
    if ip.lower().startswith("::1"):
        return True
    if re.match(r"^fc[0-9a-f]{1}::", ip.lower()):
        return True

    return False


def _is_trusted_domain(host: str) -> bool:
    """
    Validate that the hostname belongs to one of the trusted domains.
    """
    host = host.lower()
    if host in TRUSTED_DOMAINS:
        return True
    if ALLOW_SUBDOMAINS:
        for domain in TRUSTED_DOMAINS:
            if host.endswith("." + domain):
                return True
    return False


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def check_api_link(api_link: str) -> str:
    """
    Validate an API URL and ensure it points to a trusted external service.
    
    Parameters
    ----------
    api_link : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an untrusted domain,
        or resolves to a private/internal IP address.
    """
    if not isinstance(api_link, str):
        raise ValueError("api_link must be a string")

    parsed = urlparse(api_link)

    # Basic URL sanity checks
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Domain trust check
    if not _is_trusted_domain(parsed.hostname):
        raise ValueError(f"Hostname {parsed.hostname!r} is not in the list of trusted domains")

    # Resolve hostname to IP(s) and ensure none are internal
    try:
        addr_info = socket.getaddrinfo(parsed.hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Failed to resolve hostname {parsed.hostname!r}: {exc}") from exc

    for entry in addr_info:
        ip = entry[4][0]
        if _is_internal_ip(ip):
            raise ValueError(f"Resolved IP {ip!r} for host {parsed.hostname!r} is internal or reserved")

    # If all checks pass, return the original URL
    return api_link