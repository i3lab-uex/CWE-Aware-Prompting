import socket
import urllib.parse
from ipaddress import ip_address, IPv4Address, IPv6Address

# ------------------------------------------------------------------
# Allowed public API domains – add or remove entries as needed
# ------------------------------------------------------------------
ALLOWED_DOMAINS = {
    "api.example.com",
    "webhooks.myservice.org",
    "services.public.net"
}

# ------------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------------
def _is_private_ip(ip: str) -> bool:
    """
    Return True if the given IP address string resolves to a private,
    loopback, or link-local address.
    """
    try:
        addr = ip_address(ip)
    except ValueError:
        # Not a valid IP address
        return True

    return (
        addr.is_loopback or
        addr.is_private or
        addr.is_link_local or
        addr.is_reserved
    )

def _resolve_host(host: str) -> list[str]:
    """
    Resolve the host to a list of IP addresses.
    Raises socket.gaierror if resolution fails.
    """
    return socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def validate_webhook_url(webhook_endpoint: str) -> str:
    """
    Validate a webhook URL received from an external service.

    Parameters
    ----------
    webhook_endpoint : str
        The raw URL supplied by the external service.

    Returns
    -------
    str
        A sanitized, validated URL that can be safely used for internal API calls.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a private/internal network, or its domain
        is not in the approved list.
    """
    # Parse the URL and perform basic sanity checks
    parsed = urllib.parse.urlparse(webhook_endpoint)
    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain)")

    # Extract the hostname (handles IPv6 addresses in brackets)
    host = parsed.hostname
    if not host:
        raise ValueError("Could not determine hostname from URL")

    # Domain whitelist check (case‑insensitive)
    if host.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not allowed")

    # Resolve the hostname to IP addresses and ensure none are private
    try:
        addr_info = _resolve_host(host)
    except socket.gaierror as exc:
        raise ValueError(f"DNS resolution failed for {host}") from exc

    # If any resolved IP is private, reject the URL
    for entry in addr_info:
        ip_str = entry[4][0]
        if _is_private_ip(ip_str):
            raise ValueError(f"URL resolves to a private IP address: {ip_str}")

    # Reconstruct the URL to guarantee no hidden components
    sanitized = urllib.parse.urlunparse((
        parsed.scheme.lower(),
        parsed.netloc,
        parsed.path or "",
        "",          # params
        parsed.query,  # keep query string as provided
        ""           # fragment (removed for safety)
    ))

    return sanitized

# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
# if __name__ == "__main__":
#     try:
#         url = validate_webhook_url("https://api.example.com/webhook?token=abc")
#         print(f"Validated URL: {url}")
#     except ValueError as e:
#         print(f"Validation failed: {e}")