import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of domains considered trusted for external API calls.
TRUSTED_DOMAINS = {
    "api.openai.com",
    "api.github.com",
    "auth.example.com",
    # add more trusted domains here
}

# Regular expression to validate a URL scheme (http or https).
URL_SCHEME_RE = re.compile(r"^(https?)://", re.IGNORECASE)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private, loopback, link-local or otherwise
    considered internal/sensitive."""
    try:
        ip_obj = ipaddress.ip_address(ip)
        return (
            ip_obj.is_private
            or ip_obj.is_loopback
            or ip_obj.is_link_local
            or ip_obj.is_reserved
            or ip_obj.is_multicast
        )
    except ValueError:
        # Not a valid IP address.
        return False


def _resolve_hostname(hostname: str) -> list[str]:
    """Return a list of resolved IP addresses for the hostname."""
    try:
        return socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return []


def check_api_link(api_link: str) -> str:
    """
    Validate an API URL to ensure it points to a trusted external domain and
    does not resolve to any internal or private IP addresses.

    Args:
        api_link: The API URL string to validate.

    Returns:
        A normalized, validated URL string.

    Raises:
        ValueError: If the URL is not HTTPS, does not belong to a trusted domain,
                    or resolves to an internal/private IP address.
    """
    # Basic scheme validation
    if not URL_SCHEME_RE.match(api_link):
        raise ValueError("URL must use http or https scheme")

    parsed = urlparse(api_link)

    # Ensure the hostname is present
    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    # Enforce HTTPS for external API calls
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed for external API calls")

    # Check if hostname is in the list of trusted domains
    host_lower = parsed.hostname.lower()
    if host_lower not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host_lower}' is not trusted")

    # Resolve hostname to IP addresses and check for private/internal IPs
    addrinfo = _resolve_hostname(host_lower)
    if not addrinfo:
        raise ValueError(f"Could not resolve hostname: {host_lower}")

    for info in addrinfo:
        ip = info[4][0]
        if _is_private_ip(ip):
            raise ValueError(
                f"Resolved IP '{ip}' for hostname '{host_lower}' is private or internal"
            )

    # Reconstruct the URL to ensure it has a clean form
    cleaned_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            "",  # params
            parsed.query,
            parsed.fragment,
        )
    )

    return cleaned_url


# Example usage (remove or comment out in production):
if __name__ == "__main__":
    try:
        valid_url = check_api_link("https://api.openai.com/v1/chat/completions")
        print(f"Validated URL: {valid_url}")
    except ValueError as exc:
        print(f"Validation error: {exc}")