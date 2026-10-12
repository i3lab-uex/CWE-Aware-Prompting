import re
import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# ------------------------------------------------------------------
# Configuration: set of domains that are explicitly allowed.
# ------------------------------------------------------------------
APPROVED_DOMAINS = {
    "api.example.com",
    "data.service.org",
    # Add more approved domains here
}

# ------------------------------------------------------------------
# Helper: check whether an IP address is in a private or reserved range.
# ------------------------------------------------------------------
def _is_private_ip(ip: str) -> bool:
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_reserved
    except ValueError:
        # Invalid IP format – treat as unsafe
        return True

# ------------------------------------------------------------------
# Main function: verify that the URL points to an approved external API.
# ------------------------------------------------------------------
def verify_api_link(url_to_check: str) -> str:
    """
    Validate that *url_to_check* points to an approved external API.
    
    The function performs the following checks:
        1. URL is syntactically valid and uses http/https.
        2. Hostname resolves to at least one public IP address.
        3. The hostname is in the list of approved domains.
    
    Returns:
        The normalized URL if all checks pass.
    
    Raises:
        ValueError: If any of the above checks fail.
    """
    # 1. Parse and validate scheme
    parsed = urlparse(url_to_check)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # 2. Validate hostname
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # 3. Resolve hostname to IP addresses
    try:
        addrinfo = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{host}': {exc}") from exc

    # 4. Ensure at least one public IP address
    for family, _, _, _, sockaddr in addrinfo:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            continue
        # Found a public IP; accept
        break
    else:
        raise ValueError(f"Hostname '{host}' resolves only to private/reserved IPs")

    # 5. Check against approved domain list
    #   Allow subdomains of approved domains (e.g., api.example.com)
    if not any(host == domain or host.endswith("." + domain) for domain in APPROVED_DOMAINS):
        raise ValueError(f"Hostname '{host}' is not an approved domain")

    # 6. Reconstruct the URL to normalise it
    normalized = urlunparse(parsed._replace(netloc=host))
    return normalized

# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
# if __name__ == "__main__":
#     try:
#         print(verify_api_link("https://api.example.com/v1/data"))
#     except ValueError as e:
#         print(f"Invalid URL: {e}")