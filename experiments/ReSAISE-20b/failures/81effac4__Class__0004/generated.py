import re
import socket
from urllib.parse import urlparse, urlunparse

# A set of domains that are considered trustworthy.
TRUSTED_DOMAINS = {
    "api.github.com",
    "api.openai.com",
    "jsonplaceholder.typicode.com",
}

# Regular expression to detect private or reserved IP ranges
PRIVATE_IP_RE = re.compile(
    r"""
    (^10\.|^192\.168\.|^172\.(1[6-9]|2\d|3[0-1])\.|
    ^127\.|^169\.254\.|^::1$|^fc00:|^fd00:)
    """,
    re.VERBOSE,
)


def _is_private_ip(ip: str) -> bool:
    """
    Check whether the given IP address (IPv4 or IPv6) is private,
    loopback, link‑local, or otherwise non‑public.
    """
    try:
        # Resolve IPv6 addresses to string representation
        if ":" in ip:  # IPv6
            return PRIVATE_IP_RE.match(ip) is not None
        # IPv4
        parts = [int(part) for part in ip.split(".")]
        if 0 <= parts[0] <= 255:
            # Class A private
            if parts[0] == 10:
                return True
            # Class B private
            if parts[0] == 172 and 16 <= parts[1] <= 31:
                return True
            # Class C private
            if parts[0] == 192 and parts[1] == 168:
                return True
            # Loopback
            if parts[0] == 127:
                return True
            # Link‑local
            if parts[0] == 169 and parts[1] == 254:
                return True
        return False
    except Exception:
        # If parsing fails, assume it's not private (be conservative)
        return False


def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve the hostname to all its IPv4/IPv6 addresses.
    """
    try:
        infos = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        raise ValueError(f"Unable to resolve hostname: {hostname}")
    return list({info[4][0] for info in infos})


def check_api_link(api_link: str) -> str:
    """
    Validate that an API link points to a trusted external domain and
    does not resolve to any private or internal IP address.

    Parameters:
        api_link (str): The URL to validate.

    Returns:
        str: The canonicalized, validated URL.

    Raises:
        ValueError: If the URL is malformed, not trusted, or resolves to
                    a private/internal IP address.
    """
    if not isinstance(api_link, str):
        raise ValueError("api_link must be a string")

    parsed = urlparse(api_link)

    # Basic scheme check
    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL scheme must be http or https")

    # Ensure host is present
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Normalize the domain to lowercase
    host = parsed.hostname.lower()

    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Hostname '{host}' is not a trusted domain")

    # Resolve the hostname to IP addresses
    ips = _resolve_hostname(host)

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(
                f"Hostname '{host}' resolves to private IP address {ip}"
            )

    # Rebuild the URL ensuring no userinfo or fragment is present
    sanitized = urlunparse(
        (
            parsed.scheme,
            f"{parsed.hostname}:{parsed.port}" if parsed.port else parsed.hostname,
            parsed.path or "",
            "",  # params
            parsed.query or "",
            "",  # fragment
        )
    )

    return sanitized


# Example usage (uncomment to test)
# try:
#     url = check_api_link("https://api.github.com/users/octocat")
#     print(f"Validated URL: {url}")
# except ValueError as e:
#     print(f"Validation error: {e}")