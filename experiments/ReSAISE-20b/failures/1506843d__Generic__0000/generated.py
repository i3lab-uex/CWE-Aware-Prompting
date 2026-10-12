import re
import socket
from urllib.parse import urlparse, ParseResult
import ipaddress

# A small whitelist of trusted API domains.
TRUSTED_DOMAINS = {
    "api.example.com",
    "services.mycompany.org",
    "data.provider.net",
}

# Regular expression to detect IPv4 or IPv6 addresses in the netloc.
IP_PATTERN = re.compile(r"^\[?[0-9a-fA-F:.]+\]?$")


def _is_private_ip(ip: str) -> bool:
    """
    Return True if the given IP string is private, loopback,
    link-local or otherwise non‑public.
    """
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return True  # Treat malformed IPs as unsafe
    return addr.is_private or addr.is_loopback or addr.is_link_local


def _resolve_host_to_ips(host: str) -> set[str]:
    """
    Resolve the host to all IPv4 and IPv6 addresses.
    Return a set of IP strings.
    """
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return set()
    return {info[4][0] for info in infos}


def inspect_api_url(url_to_inspect: str) -> str:
    """
    Validate that the supplied URL points to a trusted external API.

    Parameters
    ----------
    url_to_inspect : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it passes validation.

    Raises
    ------
    ValueError
        If the URL is not HTTPS, points to an untrusted domain,
        or resolves to a private/internal IP address.
    """
    # Basic scheme check
    parsed: ParseResult = urlparse(url_to_inspect)
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed for external APIs.")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain).")

    host = parsed.hostname
    if not host:
        raise ValueError("Unable to extract hostname from URL.")

    # Detect direct IP usage in the netloc
    if IP_PATTERN.match(host):
        raise ValueError("Direct IP addresses are not allowed in the URL.")

    # Check against trusted domain list
    if host.lower() not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the list of trusted API domains.")

    # Resolve host to IP addresses and ensure none are private
    resolved_ips = _resolve_host_to_ips(host)
    if not resolved_ips:
        raise ValueError(f"Could not resolve host '{host}'.")
    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' for host '{host}' is not publicly accessible.")

    # All checks passed – return the original URL
    return url_to_inspect

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    test_url = "https://api.example.com/v1/data"
    try:
        validated = inspect_api_url(test_url)
        print(f"Validated URL: {validated}")
    except ValueError as exc:
        print(f"URL validation failed: {exc}")