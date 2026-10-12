import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# --------------------------------------------------------------------------- #
# Trusted domains configuration – update as needed for your environment.
TRUSTED_DOMAINS = [
    r'^api\.example\.com$',          # exact match
    r'^services\.trusted\.org$',
    r'^api\.partner\d+\.com$',       # wildcard partner domains
]
# --------------------------------------------------------------------------- #

def _is_ip_private(ip: str) -> bool:
    """
    Return True if the given IP string resolves to a private, reserved,
    or loopback address that should not be accessed from the public network.
    """
    try:
        ip_obj = ipaddress.ip_address(ip)
        return (
            ip_obj.is_private or
            ip_obj.is_loopback or
            ip_obj.is_reserved or
            ip_obj.is_multicast or
            ip_obj.is_link_local
        )
    except ValueError:
        # Not a valid IP address – treat as non‑private
        return False

def _get_resolved_ips(hostname: str) -> list[str]:
    """
    Resolve a hostname to all IPv4/IPv6 addresses.
    Raises socket.gaierror if resolution fails.
    """
    try:
        # getaddrinfo returns tuples of (family, type, proto, canonname, sockaddr)
        infos = socket.getaddrinfo(hostname, None, family=socket.AF_UNSPEC, type=socket.SOCK_STREAM)
        return [info[4][0] for info in infos]
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

def _is_trusted_hostname(hostname: str) -> bool:
    """
    Check if the hostname matches one of the trusted domain patterns.
    """
    for pattern in TRUSTED_DOMAINS:
        if re.match(pattern, hostname, flags=re.IGNORECASE):
            return True
    return False

def verify_api_address(url_to_check: str) -> str:
    """
    Validate that a given URL points to an external, trusted API endpoint.

    Parameters
    ----------
    url_to_check : str
        The URL to validate.

    Returns
    -------
    str
        A normalized, validated URL ready for use in outbound requests.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        resolves to a private/internal IP address,
        or does not belong to a trusted domain.
    """
    # 1. Basic parsing and scheme check
    parsed = urlparse(url_to_check)
    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported or missing scheme in URL: {url_to_check}")

    # 2. Ensure hostname is present
    if not parsed.hostname:
        raise ValueError(f"No hostname found in URL: {url_to_check}")

    # 3. Reject URLs that embed IP addresses directly
    try:
        ipaddress.ip_address(parsed.hostname)
        # If the hostname is an IP address, check if it is private
        if _is_ip_private(parsed.hostname):
            raise ValueError(f"URL points to a private IP address: {url_to_check}")
    except ValueError:
        # Not an IP literal – proceed with DNS resolution
        pass

    # 4. Resolve hostname and ensure none of the resolved IPs are private
    resolved_ips = _get_resolved_ips(parsed.hostname)
    for ip in resolved_ips:
        if _is_ip_private(ip):
            raise ValueError(
                f"Resolved IP {ip} for hostname '{parsed.hostname}' "
                "is private or otherwise disallowed."
            )

    # 5. Validate that the hostname matches one of the trusted patterns
    if not _is_trusted_hostname(parsed.hostname):
        raise ValueError(
            f"Hostname '{parsed.hostname}' is not in the list of trusted domains."
        )

    # 6. Reconstruct a clean URL (strip fragments, normalize case)
    cleaned = parsed._replace(fragment="")  # remove fragment
    validated_url = urlunparse(cleaned)

    return validated_url

# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only):
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/v1/data",
        "http://services.trusted.org/api?query=123",
        "https://api.partner2.com/resource#section",
        "http://192.168.1.10/secret",           # should fail
        "https://malicious.com/api",            # should fail
    ]

    for url in test_urls:
        try:
            print(f"Validating: {url}")
            result = verify_api_address(url)
            print(f"  ✅ Validated URL: {result}\n")
        except ValueError as e:
            print(f"  ❌ Validation error: {e}\n")