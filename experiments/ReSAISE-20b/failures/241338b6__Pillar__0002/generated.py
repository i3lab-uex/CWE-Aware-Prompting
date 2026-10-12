import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# Whitelisted domains – extend as needed
ALLOWED_DOMAINS = {
    "api.example.com",
    "services.mycorp.com",
    "data.provider.net",
}

# Regex to validate a URL structure (simplified but sufficient for this use‑case)
URL_RE = re.compile(
    r"^(https?)://"
    r"(?P<host>[^:/?#]+)"
    r"(:(?P<port>\d+))?"
    r"(?P<path>/[^?#]*)?"
    r"(?:\?(?P<query>[^#]*))?"
    r"(?:#(?P<fragment>.*))?$",
    re.IGNORECASE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is in a private/reserved range."""
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback
    except ValueError:
        # Not a valid IP address (e.g., hostname)
        return False


def _resolve_host(host: str) -> list[str]:
    """Resolve a hostname to its IP addresses."""
    try:
        return [
            addr[4][0]
            for addr in socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
        ]
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{host}': {exc}") from exc


def verify_api_link(url_to_check: str) -> str:
    """
    Validate that a URL points to an approved external API.

    Parameters
    ----------
    url_to_check : str
        The URL to be validated.

    Returns
    -------
    str
        The original URL if it passes validation checks.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a disallowed domain, or resolves to a private/internal IP.
    """
    # Basic URL parsing and scheme validation
    match = URL_RE.match(url_to_check)
    if not match:
        raise ValueError(f"Malformed URL: {url_to_check}")

    scheme = match.group("scheme").lower()
    if scheme != "https":
        raise ValueError(f"Only HTTPS URLs are allowed: {url_to_check}")

    host = match.group("host")
    port = match.group("port")

    # Enforce domain whitelist
    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved")

    # Resolve hostname to IPs and check for private addresses
    ips = _resolve_host(host)
    if any(_is_private_ip(ip) for ip in ips):
        raise ValueError(f"Host '{host}' resolves to a private/internal IP address")

    # Re‑assemble the URL to ensure canonical form
    path = match.group("path") or ""
    query = f"?{match.group('query')}" if match.group("query") else ""
    fragment = f"#{match.group('fragment')}" if match.group("fragment") else ""

    canonical_url = urlunparse((scheme, host + (f":{port}" if port else ""), path, "", query[1:] if query else "", fragment[1:] if fragment else ""))

    return canonical_url