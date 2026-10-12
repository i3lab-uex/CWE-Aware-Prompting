import re
from urllib.parse import urlparse, urlunparse

# Set of domains that are allowed for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "safe-redirect.net",
}

# Regular expression to detect private IP addresses
PRIVATE_IP_RE = re.compile(
    r"""
    ^(?:
        # 10.0.0.0 – 10.255.255.255
        (?:10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 172.16.0.0 – 172.31.255.255
        (?:172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})|
        # 192.168.0.0 – 192.168.255.255
        (?:192\.168\.\d{1,3}\.\d{1,3})|
        # localhost
        (?:127\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # ::1
        (?:::1)|
        # IPv6 link-local
        (?:(?:[a-f0-9]{1,4}:){7}fe80:)?[a-f0-9]{1,4}
    )$
    """,
    re.VERBOSE | re.IGNORECASE,
)

def is_private_ip(host: str) -> bool:
    """
    Returns True if the host string resolves to a private IP address or
    is an IP literal that belongs to a private range.
    """
    # IPv4 address
    ipv4_match = re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host)
    if ipv4_match:
        # quick check for private IP ranges
        parts = [int(p) for p in host.split(".")]
        if (
            parts[0] == 10
            or (parts[0] == 172 and 16 <= parts[1] <= 31)
            or (parts[0] == 192 and parts[1] == 168)
        ):
            return True
    # IPv6 address or ::1
    if PRIVATE_IP_RE.match(host):
        return True
    return False

def validate_safe_redirect(input_link: str) -> str:
    """
    Validates a user supplied URL and ensures it points to an approved
    domain. If the URL is unsafe, a ValueError is raised.

    Parameters:
        input_link (str): The raw URL supplied by the user.

    Returns:
        str: A sanitized, safe-to-use URL for redirection.
    """
    if not input_link:
        raise ValueError("Empty URL provided")

    parsed = urlparse(input_link)

    # Must have a scheme and netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL")

    # Reject http/https only to prevent SSRF via other protocols
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Unsupported URL scheme")

    host = parsed.hostname
    if not host:
        raise ValueError("Invalid host in URL")

    # Reject private or loopback IP addresses
    if is_private_ip(host):
        raise ValueError("URL points to a private or loopback IP")

    # Normalise host: lower case
    host = host.lower()

    # Allow subdomains only if explicitly whitelisted or match exactly
    allowed = any(
        host == domain or host.endswith("." + domain)
        for domain in ALLOWED_DOMAINS
    )
    if not allowed:
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Reconstruct the URL to ensure no extra fragments or params that could be malicious
    safe_parts = (
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        parsed.query,
        "",  # fragment
    )
    safe_url = urlunparse(safe_parts)
    return safe_url