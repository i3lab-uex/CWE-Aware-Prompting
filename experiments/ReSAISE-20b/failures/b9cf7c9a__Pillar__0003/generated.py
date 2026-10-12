import re
from urllib.parse import urlparse
import socket
import ipaddress

# --------------------------------------------------------------------
# Configuration – list of approved domains or domain patterns.
# Add any external API hostnames you trust here.  Patterns may use
# simple glob-style wildcards (e.g., '*.api.example.com').
# --------------------------------------------------------------------
APPROVED_DOMAINS = [
    "api.openai.com",
    "*.api.example.com",
    "services.google.com",
]

# --------------------------------------------------------------------
# Helper utilities
# --------------------------------------------------------------------

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private, loopback or reserved."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address (e.g., hostname)
        return False

def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve a hostname to all its IP addresses."""
    try:
        # getaddrinfo returns tuples; we extract the IP part.
        infos = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
        return {info[4][0] for info in infos}
    except socket.gaierror:
        # DNS resolution failed
        return set()

def _matches_approved_domain(host: str) -> bool:
    """Check if the hostname matches one of the approved patterns."""
    for pattern in APPROVED_DOMAINS:
        # Simple wildcard support: '*.example.com' matches subdomains
        if pattern.startswith("*."):
            suffix = pattern[2:]
            if host.endswith("." + suffix) or host == suffix:
                return True
        else:
            if host.lower() == pattern.lower():
                return True
    return False

# --------------------------------------------------------------------
# Main validation function
# --------------------------------------------------------------------

def check_api_url(endpoint_url: str) -> str:
    """
    Validate that `endpoint_url` points to an approved external API.

    Parameters
    ----------
    endpoint_url : str
        The URL to be validated.

    Returns
    -------
    str
        The original URL if it is deemed safe and approved.

    Raises
    ------
    ValueError
        If the URL does not belong to an approved domain, resolves to a private
        or internal IP address, or otherwise fails validation.
    """
    if not isinstance(endpoint_url, str):
        raise ValueError("endpoint_url must be a string")

    # Parse the URL
    parsed = urlparse(endpoint_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL format: {endpoint_url}")

    # Disallow non-HTTP/HTTPS schemes
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL does not contain a valid host")

    # 1. Domain whitelist check
    if not _matches_approved_domain(hostname):
        raise ValueError(f"Domain '{hostname}' is not in the approved list")

    # 2. Resolve hostname and ensure no private IPs are returned
    ips = _resolve_hostname(hostname)
    if not ips:
        raise ValueError(f"Could not resolve hostname: {hostname}")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(
                f"Resolved IP {ip} for host '{hostname}' is private or internal"
            )

    # All checks passed
    return endpoint_url

# --------------------------------------------------------------------
# Example usage (commented out – remove comments to test)
# --------------------------------------------------------------------
# if __name__ == "__main__":
#     try:
#         safe_url = check_api_url("https://api.openai.com/v1/chat/completions")
#         print(f"URL is safe: {safe_url}")
#     except ValueError as e:
#         print(f"URL validation failed: {e}")