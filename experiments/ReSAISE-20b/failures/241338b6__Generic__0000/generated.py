import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# A list of domains that are allowed to be used as external API endpoints.
ALLOWED_DOMAINS = {
    "api.openai.com",
    "api.example.com",
    "services.somecorp.io",
}

# Regular expression for matching URLs that use an IP address directly.
IP_URL_RE = re.compile(r"^(?P<scheme>https?)://(?P<host>\d{1,3}(?:\.\d{1,3}){3})(?P<port>:\d+)?(?P<path>/.*)?$")


def _is_private_ip(host: str) -> bool:
    """
    Return True if the given host resolves to a private IP address.
    """
    try:
        # Resolve all addresses for the hostname
        addr_info = socket.getaddrinfo(host, None)
    except socket.gaierror:
        # If we cannot resolve the host, treat it as unsafe
        return True

    for _, _, _, _, sockaddr in addr_info:
        ip_str = sockaddr[0]
        try:
            ip_obj = ipaddress.ip_address(ip_str)
        except ValueError:
            continue
        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
            return True
    return False


def _is_allowed_domain(host: str) -> bool:
    """
    Return True if the host matches one of the allowed domains.
    Subdomains are also accepted if they end with an allowed domain.
    """
    host = host.lower()
    return any(host == d or host.endswith("." + d) for d in ALLOWED_DOMAINS)


def verify_api_link(url_to_check: str) -> str:
    """
    Validate that the given URL points to an approved external API.

    Parameters
    ----------
    url_to_check : str
        The URL to validate.

    Returns
    -------
    str
        A normalized, validated URL that points to an approved external API.

    Raises
    ------
    ValueError
        If the URL does not belong to an approved domain or if it resolves to a private/internal IP.
    """
    # Basic URL parsing
    parsed = urlparse(url_to_check)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http and https are allowed.")

    # If the host is an IP address, ensure it is not private
    if IP_URL_RE.match(url_to_check):
        host = parsed.hostname
        if _is_private_ip(host):
            raise ValueError(f"URL resolves to a private IP address: {host}")

    # If the host is a hostname, ensure it resolves to a public IP and belongs to an allowed domain
    else:
        host = parsed.hostname or ""
        if not _is_allowed_domain(host):
            raise ValueError(f"Domain '{host}' is not in the list of approved domains.")
        if _is_private_ip(host):
            raise ValueError(f"Domain '{host}' resolves to a private IP address.")

    # Reconstruct the URL to ensure consistent formatting
    cleaned = urlunparse(parsed._replace(netloc=parsed.netloc.lower()))
    return cleaned