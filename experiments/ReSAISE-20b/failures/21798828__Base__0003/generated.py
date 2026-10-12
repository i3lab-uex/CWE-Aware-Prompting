import re
import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# List of approved API domains (exact match or subdomains)
APPROVED_DOMAINS = {
    "api.example.com",
    "service.internal.company.com",
}

# Regular expression to reject private IP ranges in the host part
PRIVATE_IP_REGEX = re.compile(
    r"""
    (?: # IPv4 private ranges
        10(?:\.\d{1,3}){3}|
        172\.1[6-9](?:\.\d{1,3}){2}|
        172\.2[0-9](?:\.\d{1,3}){2}|
        172\.3[0-1](?:\.\d{1,3}){2}|
        192\.168(?:\.\d{1,3}){2}
    ) |
    (?: # IPv6 private ranges
        fd[0-9a-f]{2}:[0-9a-f:]+|
        fe80:[0-9a-f:]+
    )
    """,
    re.VERBOSE | re.IGNORECASE,
)


def _is_private_ip(host: str) -> bool:
    """
    Determine if the host resolves to a private IP address.
    """
    try:
        # Resolve all addresses for the host
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        # If resolution fails treat as unsafe
        return True

    for family, _, _, _, sockaddr in infos:
        if family == socket.AF_INET:  # IPv4
            ip = ipaddress.IPv4Address(sockaddr[0])
        elif family == socket.AF_INET6:  # IPv6
            ip = ipaddress.IPv6Address(sockaddr[0])
        else:
            continue

        if ip.is_private or ip.is_loopback or ip.is_link_local:
            return True
    return False


def _is_approved_domain(host: str) -> bool:
    """
    Check if the host is in the approved domain list.
    Subdomains are allowed if the base domain matches.
    """
    host = host.lower()
    # Exact match
    if host in APPROVED_DOMAINS:
        return True

    # Subdomain check
    for domain in APPROVED_DOMAINS:
        if host.endswith("." + domain):
            return True
    return False


def handle_webhook(webhook_link: str) -> str:
    """
    Validate a webhook URL and return it if it references an approved
    internal API endpoint.

    Parameters:
        webhook_link (str): URL provided by the external service.

    Returns:
        str: The validated URL.

    Raises:
        ValueError: If the URL is malformed, points to a private
                    network address, or targets an unapproved domain.
    """
    # Basic parsing
    parsed = urlparse(webhook_link)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL: missing scheme or host")

    # Reject non-HTTPS URLs to avoid accidental plain HTTP requests
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # Reject hosts that look like IP addresses or private ranges
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", parsed.hostname or ""):
        if _is_private_ip(parsed.hostname):
            raise ValueError("URL points to a private IP address")
    elif PRIVATE_IP_REGEX.search(parsed.hostname or ""):
        raise ValueError("URL contains private IP pattern")

    # Validate host against approved domains
    if not _is_approved_domain(parsed.hostname or ""):
        raise ValueError(f"Domain '{parsed.hostname}' is not approved")

    # Reconstruct URL to normalize (remove default ports, etc.)
    cleaned = parsed._replace(netloc=parsed.hostname)
    return urlunparse(cleaned)


# Example usage (for testing purposes only)
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/v1/data",
        "http://api.example.com/v1/data",          # Should fail (non-HTTPS)
        "https://10.0.0.5/api",                   # Should fail (private IP)
        "https://malicious.com/evil",              # Should fail (unapproved domain)
    ]

    for url in test_urls:
        try:
            print(f"Validating: {url}")
            result = handle_webhook(url)
            print("  => Valid:", result)
        except ValueError as e:
            print("  => Invalid:", e)