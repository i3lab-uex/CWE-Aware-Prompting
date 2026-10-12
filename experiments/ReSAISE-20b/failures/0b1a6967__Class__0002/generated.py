import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# ------------------------------------------------------------
# Configuration: list of approved domains.  Add or remove as needed.
# ------------------------------------------------------------
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.company.com",
}

# ------------------------------------------------------------
# Regular expressions for detecting potentially unsafe hostnames
# ------------------------------------------------------------
LOCALHOST_RE = re.compile(r"^(localhost|127\.0\.0\.1|::1)$", re.IGNORECASE)
LOCALDOMAIN_RE = re.compile(r"\.(local|internal|corp|lan|private)$", re.IGNORECASE)
PROXY_RE = re.compile(r"^proxy\.example\.com$", re.IGNORECASE)  # add known proxy hosts

# ------------------------------------------------------------
def _is_private_ip(ip_str: str) -> bool:
    """
    Determine if the given IP string is in a private or reserved range.
    """
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
    except ValueError:
        # Not an IP address
        return False

def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve a hostname to all associated IP addresses.
    If resolution fails, return an empty list.
    """
    try:
        infos = socket.getaddrinfo(hostname, None)
        return list({sock[4][0] for sock in infos})
    except socket.gaierror:
        return []

def _is_hostname_allowed(hostname: str) -> bool:
    """
    Check if the hostname is allowed according to whitelist and
    various safety rules.
    """
    # Reject obvious localhost / private addresses
    if LOCALHOST_RE.match(hostname) or PROXY_RE.match(hostname):
        return False

    # Reject domain names that end with reserved TLDs
    if LOCALDOMAIN_RE.search(hostname):
        return False

    # Check against explicit whitelist
    if hostname.lower() in ALLOWED_DOMAINS:
        return True

    # Resolve and inspect IPs
    ips = _resolve_hostname(hostname)
    if not ips:
        # If we cannot resolve, be conservative
        return False

    for ip in ips:
        if _is_private_ip(ip):
            return False
    # If all resolved IPs are public, allow it
    return True

def verify_api_address(endpoint_address: str) -> str:
    """
    Validate that the given URL points to a secure, external API endpoint.

    Parameters
    ----------
    endpoint_address : str
        The URL that needs to be verified.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, does not use HTTPS, points to a disallowed domain,
        or resolves to an internal/private address.
    """
    # Basic parsing
    parsed = urlparse(endpoint_address)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL format: {endpoint_address}")

    # Enforce HTTPS
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed to prevent SSRF via HTTP")

    # Strip default ports for consistency
    netloc = parsed.netloc.split(":")[0]

    # Validate hostname
    if not _is_hostname_allowed(netloc):
        raise ValueError(f"Hostname '{netloc}' is not allowed")

    # Reconstruct canonical URL (drop default ports, normalise)
    cleaned = parsed._replace(netloc=netloc).geturl()
    return cleaned

# ------------------------------------------------------------
# Example usage (remove or comment out in production)
# ------------------------------------------------------------
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/v1/data",
        "http://malicious.internal/api",
        "https://127.0.0.1:8000/endpoint",
        "https://proxy.example.com/api",
    ]

    for url in test_urls:
        try:
            verified = verify_api_address(url)
            print(f"✅ {url} → {verified}")
        except ValueError as exc:
            print(f"❌ {url} → {exc}")