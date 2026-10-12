import ipaddress
from urllib.parse import urlparse, urlunparse

# Allowed public API domains. Extend as needed.
ALLOWED_DOMAINS = {
    "api.example.com",
    "webhook.services.com",
    "hooks.myapp.io",
}

# IPv4 and IPv6 private address blocks
PRIVATE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),  # Unique local address
]


def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address string is private or reserved."""
    try:
        ip_obj = ipaddress.ip_address(ip)
        return any(ip_obj in net for net in PRIVATE_IP_RANGES)
    except ValueError:
        # Not an IP address
        return False


def _is_allowed_domain(host: str) -> bool:
    """Check if the host is in the allowed domain list."""
    # Resolve subdomains: only exact matches are permitted
    return host in ALLOWED_DOMAINS


def validate_webhook_url(webhook_endpoint: str) -> str:
    """
    Validate a webhook URL provided by an external service.

    Parameters
    ----------
    webhook_endpoint : str
        The raw URL supplied by the external service.

    Returns
    -------
    str
        A sanitized URL that can be safely used for internal API requests.

    Raises
    ------
    ValueError
        If the URL's domain is not in the allowed list or if it resolves to a private IP.
    """
    # Parse the URL and ensure scheme is http or https
    parsed = urlparse(webhook_endpoint)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject private or reserved IP addresses
    if _is_private_ip(host):
        raise ValueError("URL points to a private network address")

    # Resolve hostname to IP(s) if needed (optional, can be commented out)
    try:
        import socket

        ips = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
        for _, _, _, _, sockaddr in ips:
            ip_str = sockaddr[0]
            if _is_private_ip(ip_str):
                raise ValueError("URL resolves to a private IP address")
    except Exception:
        # If DNS resolution fails, we simply keep the hostname check
        pass

    # Ensure domain is allowed
    if not _is_allowed_domain(host):
        raise ValueError(f"Domain '{host}' is not in the allowed list")

    # Reconstruct a clean URL (strip query params if not needed)
    cleaned = urlunparse(
        (
            parsed.scheme,
            f"{host}:{parsed.port}" if parsed.port else host,
            parsed.path or "/",
            "",  # params
            "",  # query
            "",  # fragment
        )
    )
    return cleaned


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     try:
#         safe_url = validate_webhook_url("https://api.example.com/webhook?token=abc")
#         print(safe_url)
#     except ValueError as e:
#         print(f"Invalid webhook URL: {e}")