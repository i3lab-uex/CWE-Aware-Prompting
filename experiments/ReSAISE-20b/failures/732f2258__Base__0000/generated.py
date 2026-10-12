import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Whitelisted public API domains (example list)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.allowed.org",
    "https://public.api.net",  # include scheme if needed
}

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:
        (?:10\.|192\.168\.)          # 10.x.x.x or 192.168.x.x
        \d{1,3}\.\d{1,3}             # any 2 octets
        |
        172\.(?:1[6-9]|2\d|3[0-1])\.   # 172.16-31.x
        \d{1,3}
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(host: str) -> bool:
    """
    Check if the host string is a private IP address.
    Accepts dotted decimal or IPv6 notation.
    """
    try:
        # Resolve host to IP; if it is already an IP, skip DNS
        ip = ipaddress.ip_address(host)
    except ValueError:
        # Not a literal IP, cannot be checked here
        return False

    return ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved


def analyze_webhook(webhook_address: str) -> str:
    """
    Validate and sanitize a webhook URL.

    Parameters
    ----------
    webhook_address : str
        The raw URL supplied by an external service.

    Returns
    -------
    str
        A validated and safe URL that can be used for internal API requests.

    Raises
    ------
    ValueError
        If the URL domain is not in the allowed list or if it points to a private network.
    """
    # Parse the URL
    parsed = urlparse(webhook_address)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL")

    # Ensure scheme is HTTP/HTTPS
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP/HTTPS schemes are allowed")

    # Extract hostname (without port)
    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a hostname")

    # Reject URLs that directly use an IP address
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host) or re.match(r"^\[.*\]$", host):
        if _is_private_ip(host.replace("[", "").replace("]", "")):
            raise ValueError("URL points to a private IP address")

    # Normalize the host for comparison (lowercase)
    normalized_host = host.lower()

    # Check against allowed domains
    if not any(
        (
            normalized_host == domain.lower()
            or normalized_host.endswith("." + domain.lower())
        )
        for domain in ALLOWED_DOMAINS
    ):
        raise ValueError(f"Domain '{normalized_host}' is not allowed")

    # Reconstruct the URL to ensure no hidden components
    safe_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            "",  # params
            parsed.query or "",
            "",  # fragment
        )
    )

    return safe_url

# Example usage (for testing purposes only):
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/webhook",
        "http://192.168.1.10/endpoint",
        "https://malicious.com/hack",
    ]

    for url in test_urls:
        try:
            print(f"Safe: {analyze_webhook(url)}")
        except ValueError as e:
            print(f"Rejected: {url} -> {e}")