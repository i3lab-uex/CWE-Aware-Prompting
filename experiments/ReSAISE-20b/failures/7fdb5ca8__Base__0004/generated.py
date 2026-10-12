import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# List of trusted domains / subdomains.  Add or remove as required.
TRUSTED_DOMAINS = {
    "api.example.com",
    "service.trusted.org",
    # Wildcard subdomains can be handled by checking suffixes if needed.
}

# Optional: allow wildcard patterns
def _is_domain_trusted(domain: str) -> bool:
    if domain in TRUSTED_DOMAINS:
        return True
    # allow subdomains of trusted domains (e.g., api.foo.example.com)
    for t in TRUSTED_DOMAINS:
        if domain.endswith("." + t):
            return True
    return False


def verify_api_address(url_to_check: str) -> str:
    """
    Validate that the given URL points to an external, trusted API.

    Raises:
        ValueError: If the URL is not HTTPS or HTTP,
                    if its domain is not trusted,
                    or if it resolves to a private / internal IP.
    Returns:
        The validated URL (unchanged).
    """
    parsed = urlparse(url_to_check)

    # 1. Ensure scheme is http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # 2. Ensure domain is present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location")

    # 3. Check that domain is trusted
    hostname = parsed.hostname.lower()
    if not _is_domain_trusted(hostname):
        raise ValueError(f"Domain '{hostname}' is not in the trusted list")

    # 4. Resolve hostname to IP(s)
    try:
        addr_info = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Failed to resolve hostname '{hostname}': {exc}") from exc

    # 5. Verify that each resolved IP is not private, loopback or reserved
    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        try:
            ip_obj = ipaddress.ip_address(ip)
        except ValueError as exc:
            raise ValueError(f"Invalid IP address resolved for {hostname}: {ip}") from exc

        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved or ip_obj.is_link_local:
            raise ValueError(f"Resolved IP {ip} for domain '{hostname}' is not allowed (private/internal)")

    # 6. Reconstruct the URL to ensure canonical form
    validated_url = urlunparse(parsed)
    return validated_url


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/v1/resource",
        "http://localhost:8000/api",
        "https://malicious.com/evil",
    ]
    for url in test_urls:
        try:
            print(f"Validating: {url}")
            print("->", verify_api_address(url))
        except ValueError as e:
            print(f"ERROR: {e}")