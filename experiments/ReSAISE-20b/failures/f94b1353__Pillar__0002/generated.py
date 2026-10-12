import re
from urllib.parse import urlparse, ParseResult
import socket
import ipaddress

# List of approved public API hosts (subdomains allowed)
APPROVED_HOSTS = {
    "api.example.com",
    "service.example.org",
    "webhook.api.company.net"
}

# Regex to match private IP ranges (CVE‑CWE 664 related check)
PRIVATE_IP_REGEX = re.compile(
    r"^(10\.|172\.(1[6-9]|2\d|3[0-1])\.|192\.168\.)"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or reserved."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address; treat as non-private
        return False

def _resolve_host(host: str) -> list[str]:
    """Resolve a hostname to all IPv4 addresses."""
    try:
        return [info[4][0] for info in socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)]
    except socket.gaierror:
        return []

def _is_host_approved(host: str) -> bool:
    """Check if the host is in the approved list or a subdomain of an approved host."""
    # Exact match
    if host in APPROVED_HOSTS:
        return True
    # Subdomain check
    for approved in APPROVED_HOSTS:
        if host.endswith("." + approved):
            return True
    return False

def _validate_and_sanitize(url_hook: str) -> ParseResult:
    """
    Validate the provided webhook URL and return a parsed, sanitized URL.
    Raises ValueError if validation fails.
    """
    # Basic parsing
    parsed = urlparse(url_hook)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL must use http or https scheme")

    if not parsed.netloc:
        raise ValueError("URL missing host component")

    host = parsed.hostname
    if not host:
        raise ValueError("Unable to determine hostname from URL")

    # Reject internal network hosts
    if _is_host_approved(host) is False:
        raise ValueError(f"Host '{host}' not in approved list")

    # Resolve host to IP addresses and ensure none are private
    ips = _resolve_host(host)
    if not ips:
        # If resolution fails, be conservative and reject
        raise ValueError(f"Could not resolve host '{host}'")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' for host '{host}' is private")

    # Rebuild URL to ensure consistent formatting
    sanitized = ParseResult(
        scheme=parsed.scheme,
        netloc=f"{host}:{parsed.port}" if parsed.port else host,
        path=parsed.path or "/",
        params="",
        query=parsed.query,
        fragment=""
    )
    return sanitized

def manage_webhook(url_hook: str) -> str:
    """
    Validate a webhook URL from an external service and return
    a sanitized URL that points to an approved public API endpoint.

    Parameters:
        url_hook (str): The webhook URL provided by the external service.

    Returns:
        str: A validated and sanitized URL.

    Raises:
        ValueError: If the URL is not approved or points to an internal resource.
    """
    sanitized = _validate_and_sanitize(url_hook)
    return sanitized.geturl()