import re
import socket
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------------- #
# Trusted provider whitelist – add or remove domains as needed
TRUSTED_DOMAINS = {
    r"^feed\.example\.org$",
    r"^news\.trustedsource\.com$",
    r"^blog\.secureprovider\.net$",
}

# Regular expression to match private / link-local / loopback IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:
        # 10.0.0.0 – 10.255.255.255
        (?:10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 172.16.0.0 – 172.31.255.255
        (?:172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})|
        # 192.168.0.0 – 192.168.255.255
        (?:192\.168\.\d{1,3}\.\d{1,3})|
        # 127.0.0.0 – 127.255.255.255 (loopback)
        (?:127\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 169.254.0.0 – 169.254.255.255 (link-local)
        (?:169\.254\.\d{1,3}\.\d{1,3})
    )$
    """,
    re.VERBOSE,
)

def _is_trusted_domain(hostname: str) -> bool:
    """Check if the hostname matches any trusted domain pattern."""
    for pattern in TRUSTED_DOMAINS:
        if re.match(pattern, hostname, re.IGNORECASE):
            return True
    return False

def _is_private_ip(ip: str) -> bool:
    """Determine if an IP address is in a private or restricted range."""
    return bool(PRIVATE_IP_REGEX.match(ip))

def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve the hostname to all IPv4 addresses."""
    try:
        # getaddrinfo returns a list of tuples; the fourth element is the sockaddr
        return [sock[4][0] for sock in socket.getaddrinfo(hostname, None, family=socket.AF_INET)]
    except socket.gaierror:
        return []

def secure_feed_link(rss_url: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_url : str
        The raw RSS feed URL supplied by an external source.

    Returns
    -------
    str
        A sanitized, trusted RSS feed URL that can safely be fetched.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP/HTTPS, if the hostname is not in the
        trusted whitelist, or if the resolved IP address is private/restricted.
    """
    # Parse and validate scheme
    parsed = urlparse(rss_url)
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalize hostname (lowercase) and check whitelist
    hostname = parsed.hostname.lower() if parsed.hostname else ""
    if not _is_trusted_domain(hostname):
        raise ValueError(f"Hostname '{hostname}' is not in the trusted provider list")

    # Resolve hostname to IP addresses and ensure none are private
    ips = _resolve_hostname(hostname)
    if not ips:
        raise ValueError(f"Could not resolve hostname: {hostname}")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP {ip} for hostname '{hostname}' is in a private network")

    # Reconstruct the URL without fragments (and optionally strip query if needed)
    sanitized = parsed._replace(fragment="")  # removes any fragment
    return urlunparse(sanitized)

# Example usage (commented out – remove or uncomment for testing)
# try:
#     safe_url = secure_feed_link("https://feed.example.org/rss")
#     print(f"Safe URL: {safe_url}")
# except ValueError as exc:
#     print(f"Validation failed: {exc}")