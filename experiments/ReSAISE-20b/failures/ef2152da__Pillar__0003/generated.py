import re
import socket
from urllib.parse import urlparse, urlunparse

# Whitelisted public API domains (example)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "services.myapp.org",
    "public.api.net",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_RE = re.compile(
    r"""
    ^(?:  # start of string
        (?:10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3} |            # 10.x.x.x or 127.x.x.x
        169\.254\.\d{1,3}\.\d{1,3} |                        # 169.254.x.x (link-local)
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3} |      # 172.16-31.x.x
        192\.168\.\d{1,3}\.\d{1,3} |                        # 192.168.x.x
        ::1$                                               # IPv6 loopback
    )
    """,
    re.VERBOSE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is private or reserved."""
    # IPv4
    if PRIVATE_IP_RE.match(ip):
        return True

    try:
        # Resolve IPv6 address and check for loopback
        addr_info = socket.getaddrinfo(ip, None)[0]
        if addr_info[0] == socket.AF_INET6 and ip == "::1":
            return True
    except Exception:
        # If we cannot resolve, assume it's not private (letting higher-level checks fail)
        pass

    return False


def validate_callback(callback_url: str) -> str:
    """
    Validate an external webhook URL and return a secure, fully-qualified
    URL suitable for internal API calls.

    Parameters
    ----------
    callback_url : str
        External webhook URL provided by a third‑party service.

    Returns
    -------
    str
        A validated and secure URL that is permitted for internal API usage.

    Raises
    ------
    ValueError
        If the URL's domain is not in the whitelist or if it resolves to a private IP.
    """
    # Parse the URL
    parsed = urlparse(callback_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL: missing scheme or netloc")

    # Ensure the URL uses HTTPS (or HTTP if explicitly allowed)
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Normalize hostname to lowercase
    hostname = parsed.hostname.lower()

    # Check whitelist
    if hostname not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not whitelisted")

    # Resolve the hostname to IP(s) and verify none are private
    try:
        addr_info = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

    for entry in addr_info:
        ip_address = entry[4][0]
        if _is_private_ip(ip_address):
            raise ValueError(f"Hostname '{hostname}' resolves to a private IP address")

    # Reconstruct the URL with a canonical form
    cleaned = parsed._replace(scheme=parsed.scheme.lower(), hostname=hostname)
    return urlunparse(cleaned)


# Example usage:
if __name__ == "__main__":
    try:
        secure_url = validate_callback("https://api.example.com/webhook")
        print(f"Validated URL: {secure_url}")
    except ValueError as e:
        print(f"Validation failed: {e}")