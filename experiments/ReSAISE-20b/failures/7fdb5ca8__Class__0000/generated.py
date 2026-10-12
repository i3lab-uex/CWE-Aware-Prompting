import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# List of domains that are considered trusted.
TRUSTED_DOMAINS = {
    "api.example.com",
    "services.trusted.org",
    "data.partner.net"
}

# Optional: allow the caller to provide additional trusted domains.
def _is_trusted_domain(hostname: str) -> bool:
    return hostname.lower() in TRUSTED_DOMAINS


def _is_internal_ip(ip: str) -> bool:
    """Return True if the IP address is in a private or non‑public range."""
    try:
        addr = ipaddress.ip_address(ip)
        return not addr.is_global
    except ValueError:
        # If we cannot parse the IP, treat it as unsafe.
        return True


def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve a hostname to a list of IP addresses."""
    try:
        return socket.gethostbyname_ex(hostname)[2]
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc


def verify_api_address(url_to_check: str) -> str:
    """
    Verify that a URL points to an external, trusted API endpoint.

    Parameters
    ----------
    url_to_check : str
        The URL to validate.

    Returns
    -------
    str
        The normalized, validated URL.

    Raises
    ------
    ValueError
        If the URL is not HTTP(S), does not resolve to a trusted domain,
        or resolves to an internal / private IP address.
    """
    parsed = urlparse(url_to_check)

    # 1. Ensure scheme is http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP(S) are allowed.")

    # 2. Ensure hostname is present
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname.")

    hostname = parsed.hostname.lower()

    # 3. Check if the domain is in the trusted list
    if not _is_trusted_domain(hostname):
        raise ValueError(f"Domain '{hostname}' is not in the list of trusted domains.")

    # 4. Resolve hostname to IP addresses and ensure none are internal
    ip_addresses = _resolve_hostname(hostname)
    for ip in ip_addresses:
        if _is_internal_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to internal IP address {ip}.")

    # 5. Reconstruct the URL to ensure consistent formatting
    cleaned = parsed._replace(
        scheme=parsed.scheme,
        netloc=f"{hostname}:{parsed.port}" if parsed.port else hostname,
        path=parsed.path or "/",
    )
    return urlunparse(cleaned)