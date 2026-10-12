import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# ------------------------------------------------------------------
# Configuration: list of approved public API domains.
# ------------------------------------------------------------------
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.provider.net",
    "webhook.secure.io",
}

# Regular expression to detect IP addresses in the hostname part.
_IP_RE = re.compile(r"""
    ^(?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
      |
        # IPv6
        \[?[A-Fa-f0-9:]+\]?
    )$
""", re.VERBOSE)


def _is_private_ip(ip_str: str) -> bool:
    """Return True if the IP address is in a private, loopback or link-local range."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        # Not a valid IP address; treat as non-private for safety.
        return False


def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve a hostname to all IPv4/IPv6 addresses. Raises socket.gaierror if unresolved."""
    infos = socket.getaddrinfo(hostname, None)
    return [sockaddr[0] for _, _, _, _, sockaddr in infos]


def _validate_hostname(hostname: str) -> None:
    """
    Validate that the hostname is in the allowed list and does not resolve to a private IP.
    Raises ValueError on failure.
    """
    # Reject direct IP addresses in the URL
    if _IP_RE.match(hostname):
        raise ValueError("URL must not contain a raw IP address")

    # Enforce domain whitelist
    if hostname.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not authorized")

    # Resolve the hostname and ensure no IP resolves to a private network
    for ip in _resolve_hostname(hostname):
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to a private IP ({ip})")


def analyze_webhook(webhook_address: str) -> str:
    """
    Validate a webhook URL and return it if safe for internal use.

    Parameters
    ----------
    webhook_address : str
        The URL supplied by an external service.

    Returns
    -------
    str
        A validated, canonicalized URL that can be safely used for internal API requests.

    Raises
    ------
    ValueError
        If the URL's domain is not in the allowed list, if it resolves to a private IP,
        or if the URL is malformed.
    """
    # Basic parsing
    parsed = urlparse(webhook_address)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL")

    # Only allow HTTP/HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Validate hostname
    _validate_hostname(parsed.hostname)

    # Reconstruct the URL to ensure canonical form (e.g., strip default ports)
    netloc = parsed.hostname
    if parsed.port and ((parsed.scheme == "http" and parsed.port != 80) or
                        (parsed.scheme == "https" and parsed.port != 443)):
        netloc += f":{parsed.port}"

    safe_url = urlunparse((parsed.scheme, netloc,
                           parsed.path or "", parsed.params or "",
                           parsed.query or "", parsed.fragment or ""))

    return safe_url