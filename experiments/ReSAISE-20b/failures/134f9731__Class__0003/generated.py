import re
from urllib.parse import urlparse, urlunparse
from ipaddress import ip_address, IPv4Address, IPv6Address

# Whitelisted public API domains
WHITELISTED_DOMAINS = {
    "api.example.com",
    "services.allowed.org",
    "public.api.net",
}

# Regular expression to match IPv4 and IPv6 addresses
IPV4_REGEX = re.compile(
    r"""
    ^
    (?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}
    (?:25[0-5]|2[0-4]\d|1?\d{1,2})
    $
    """,
    re.VERBOSE,
)

IPV6_REGEX = re.compile(
    r"""
    ^
    \s*
    (?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}
    |
    (?:[0-9a-fA-F]{1,4}:){1,7}:
    |
    (?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}
    |
    (?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}
    |
    (?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}
    |
    (?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}
    |
    (?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}
    |
    [0-9a-fA-F]{1,4}:(?::[0-9a-fA-F]{1,4}){1,6}
    |
    :(?::[0-9a-fA-F]{1,4}){1,7}
    |
    ::
    $
    """,
    re.VERBOSE,
)

PRIVATE_IP_RANGES = [
    # IPv4 private ranges
    ("10.0.0.0", "10.255.255.255"),
    ("172.16.0.0", "172.31.255.255"),
    ("192.168.0.0", "192.168.255.255"),
    # IPv6 unique local addresses
    ("fc00::", "fdff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"),
]

def _is_private_ip(ip_str: str) -> bool:
    """Return True if ip_str is a private IP address."""
    try:
        ip = ip_address(ip_str)
    except ValueError:
        return False
    if isinstance(ip, IPv4Address):
        for start, end in PRIVATE_IP_RANGES:
            if ip_address(start) <= ip <= ip_address(end):
                return True
    elif isinstance(ip, IPv6Address):
        # Unique local addresses fc00::/7
        if ip_address("fc00::") <= ip <= ip_address("fdff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"):
            return True
    return False

def verify_webhook(webhook_endpoint: str) -> str:
    """
    Validate an external webhook URL before it is used to initiate an internal API call.

    Parameters
    ----------
    webhook_endpoint : str
        The URL supplied by an external source.

    Returns
    -------
    str
        A sanitized, validated URL that is allowed for internal use.

    Raises
    ------
    ValueError
        If the URL domain is not whitelisted or attempts to access private network addresses.
    """
    if not isinstance(webhook_endpoint, str):
        raise ValueError("Webhook endpoint must be a string")

    parsed = urlparse(webhook_endpoint)

    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Webhook URL must use http or https scheme")

    # Resolve hostname to IPs (simple approach: check if host is an IP literal)
    host = parsed.hostname
    if not host:
        raise ValueError("Webhook URL must contain a hostname")

    # Reject IP literal addresses that are private
    if IPV4_REGEX.match(host) or IPV6_REGEX.match(host):
        if _is_private_ip(host):
            raise ValueError("Webhook URL resolves to a private IP address")

    # Normalise domain case
    host_lower = host.lower()

    if host_lower not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the whitelist")

    # Reconstruct URL to ensure no extra components (e.g., userinfo)
    sanitized = urlunparse((
        parsed.scheme,
        host_lower,
        parsed.path or "",
        "",  # params
        parsed.query or "",
        ""   # fragment
    ))

    return sanitized