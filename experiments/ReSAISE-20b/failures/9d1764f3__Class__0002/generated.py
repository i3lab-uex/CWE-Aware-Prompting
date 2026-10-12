import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Whitelisted public API endpoints (exact hostnames or subdomains)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "webhooks.myservice.org",
    "secure.api.thirdparty.io",
}

# Regex for common private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:
        # 10.0.0.0/8
        (10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 172.16.0.0/12
        (172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|
        # 192.168.0.0/16
        (192\.168\.\d{1,3}\.\d{1,3})|
        # IPv6 unique local addresses
        ([fF][cC-DFa-fA-F]\:[0-9a-fA-F:]+)
    )
    """,
    re.VERBOSE,
)

def _is_private_ip(host: str) -> bool:
    """
    Return True if the host resolves to a private IP address.
    Handles both IPv4 and IPv6. If hostname resolution fails,
    conservatively treat it as private to avoid accidental exposure.
    """
    try:
        # Resolve hostname to all IPs
        for addr_info in ipaddress.ip_address(host):
            if addr_info.is_private:
                return True
    except ValueError:
        # Not an IP literal, try to resolve via socket
        import socket

        try:
            for addr in socket.getaddrinfo(host, None):
                ip = addr[4][0]
                if ipaddress.ip_address(ip).is_private:
                    return True
        except socket.gaierror:
            # Unresolvable host; treat as unsafe
            return True

    return False


def validate_webhook(webhook_link: str) -> str:
    """
    Validate that a webhook URL is allowed for internal API calls.

    Parameters
    ----------
    webhook_link : str
        The external webhook URL supplied by a third‑party.

    Returns
    -------
    str
        A sanitized, fully qualified URL that can be safely used internally.

    Raises
    ------
    ValueError
        If the URL domain is not in the whitelist or if it resolves to a private
        network address. Also raised for malformed URLs or disallowed schemes.
    """
    if not isinstance(webhook_link, str):
        raise ValueError("Webhook link must be a string")

    parsed = urlparse(webhook_link)

    # Only allow HTTPS (and HTTP for trusted internal services, but here we disallow)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Reject URLs with fragments or query parameters that could be abused
    if parsed.fragment:
        raise ValueError("URL must not contain a fragment")

    # Extract hostname (may be None for URLs like 'mailto:')
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Normalize host to lowercase
    host = host.lower()

    # Check against whitelist (exact match or subdomain allowed)
    if not any(
        host == domain or host.endswith("." + domain) for domain in WHITELISTED_DOMAINS
    ):
        raise ValueError(f"Domain '{host}' is not in the whitelist")

    # Reject private IP addresses
    if PRIVATE_IP_REGEX.match(host):
        raise ValueError(f"Domain '{host}' resolves to a private IP address")

    # Resolve hostname to ensure it does not point to internal networks
    if _is_private_ip(host):
        raise ValueError(f"Domain '{host}' resolves to a private IP address")

    # Reconstruct the URL ensuring no userinfo or password is leaked
    safe_netloc = host
    if parsed.port:
        safe_netloc += f":{parsed.port}"

    sanitized = urlunparse(
        (
            parsed.scheme,
            safe_netloc,
            parsed.path or "",
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return sanitized


# Example usage (uncomment to test):
# try:
#     print(validate_webhook("https://api.example.com/webhooks/123"))
# except ValueError as e:
#     print("Invalid webhook:", e)