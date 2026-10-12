import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# List of approved external API domains (case‑insensitive)
APPROVED_DOMAINS = {
    "api.openai.com",
    "api.github.com",
    "api.stripe.com",
    # add more domains as needed
}

# Regular expression to detect protocols that are not HTTP/HTTPS
PROTOCOL_RE = re.compile(r"^(?!https?://).", re.IGNORECASE)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private or non‑public range."""
    try:
        addr = ipaddress.ip_address(ip)
        return not (addr.is_global and not addr.is_reserved)
    except ValueError:
        # If IP resolution fails, treat it as non‑public
        return False


def _resolve_hostname(hostname: str) -> list[str]:
    """Return a list of IP addresses for the given hostname."""
    try:
        return [info[4][0] for info in socket.getaddrinfo(hostname, None)]
    except socket.gaierror:
        return []


def verify_api_link(url_to_check: str) -> str:
    """
    Validate that a URL points to an approved external API and is not
    targeting internal or private network addresses.

    Parameters
    ----------
    url_to_check : str
        The URL to validate.

    Returns
    -------
    str
        Normalised, validated URL that points to an approved domain.

    Raises
    ------
    ValueError
        If the URL is not HTTP/HTTPS, does not resolve to an approved domain,
        or resolves to a private/internal IP address.
    """
    # Basic protocol check
    if PROTOCOL_RE.search(url_to_check):
        raise ValueError("Only http:// or https:// URLs are allowed")

    parsed = urlparse(url_to_check)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Normalise domain to lowercase for comparison
    host_lower = hostname.lower()

    if not any(host_lower.endswith(domain) for domain in APPROVED_DOMAINS):
        raise ValueError(f"Domain '{hostname}' is not in the approved list")

    # Resolve hostname to IPs and check for private addresses
    ips = _resolve_hostname(hostname)
    if not ips:
        raise ValueError(f"Could not resolve hostname: {hostname}")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname resolves to private IP {ip}")

    # Reconstruct a cleaned URL (remove user info, fragments)
    cleaned = parsed._replace(netloc=parsed.hostname + (f":{parsed.port}" if parsed.port else ""),
                              params="", query="", fragment="")
    return urlunparse(cleaned)