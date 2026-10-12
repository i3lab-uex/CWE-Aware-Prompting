import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# ----------------------------------------------------------------------
# Configuration: list of approved public API domains.
# Add any additional allowed domains here.
ALLOWED_DOMAINS = {
    "api.example.com",
    "webhooks.service.org",
    "trusted.partner.net"
}

# ----------------------------------------------------------------------
# Regular expression for detecting private IP address ranges.
PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (?:                               # start non-capturing group for the 4 patterns
        10\.\d{1,3}\.\d{1,3}\.\d{1,3} |          # 10.0.0.0 – 10.255.255.255
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3} |  # 172.16.0.0 – 172.31.255.255
        192\.168\.\d{1,3}\.\d{1,3} |              # 192.168.0.0 – 192.168.255.255
        127\.\d{1,3}\.\d{1,3}\.\d{1,3} |          # 127.0.0.0 – 127.255.255.255
        169\.254\.\d{1,3}\.\d{1,3}                # 169.254.0.0 – 169.254.255.255
    )
    $
    """,
    re.VERBOSE,
)

# ----------------------------------------------------------------------
def _is_private_ip(host: str) -> bool:
    """
    Return True if the host resolves to a private IP address.
    We perform a simple regex check for common private ranges
    and also attempt an ipaddress conversion in case the host is
    already an IP literal.
    """
    # Direct IP literal check
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        pass

    # Regex check for common private patterns (e.g., 10.0.0.1)
    return bool(PRIVATE_IP_RE.match(host))


# ----------------------------------------------------------------------
def validate_webhook_url(webhook_endpoint: str) -> str:
    """
    Validate an incoming webhook URL.

    Parameters
    ----------
    webhook_endpoint : str
        The raw URL supplied by an external service.

    Returns
    -------
    str
        A sanitized and validated URL that can be safely used for internal API requests.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a private/internal network, or has a domain not in the allowed list.
    """
    if not isinstance(webhook_endpoint, str):
        raise ValueError("Webhook endpoint must be a string")

    # Parse the URL
    parsed = urlparse(webhook_endpoint)

    # Scheme must be http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http and https are allowed.")

    # Host must be present
    if not parsed.hostname:
        raise ValueError("URL does not contain a valid hostname")

    # Reject private IP addresses or loopback
    if _is_private_ip(parsed.hostname):
        raise ValueError(f"Hostname '{parsed.hostname}' resolves to a private or internal IP address")

    # Reject if hostname is not in the approved list
    # Normalize by removing trailing dots and converting to lowercase
    hostname = parsed.hostname.rstrip(".").lower()
    if hostname not in ALLOWED_DOMAINS:
        raise ValueError(f"Hostname '{hostname}' is not an approved domain")

    # Reconstruct the URL to ensure it has no userinfo, fragments, or query parameters
    sanitized = urlunparse((
        parsed.scheme,
        f"{parsed.hostname}{':' + str(parsed.port) if parsed.port else ''}",
        parsed.path or "/",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return sanitized

# ----------------------------------------------------------------------
# Example usage (for debugging only; remove or guard with __name__ == "__main__")
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/webhook",
        "http://webhooks.service.org/notify?token=abc",  # query will be stripped
        "https://192.168.1.10/endpoint",  # should raise ValueError
        "ftp://api.example.com/resource",  # unsupported scheme
        "https://malicious.bad.com/webhook"  # domain not allowed
    ]

    for url in test_urls:
        try:
            print(f"Original: {url}\nValidated: {validate_webhook_url(url)}\n")
        except ValueError as e:
            print(f"Original: {url}\nError: {e}\n")