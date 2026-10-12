import re
from urllib.parse import urlparse, urlunparse

# List of approved public API domains (exact matches or subdomains)
APPROVED_DOMAINS = {
    "api.example.com",
    "service.mycompany.org",
}

# Regular expressions for private / reserved IP ranges
PRIVATE_IP_PATTERNS = [
    re.compile(r"^(10|127)\."),                      # 10.x.x.x, loopback
    re.compile(r"^172\.(1[6-9]|2\d|3[0-1])\.") ,     # 172.16.x.x – 172.31.x.x
    re.compile(r"^192\.168\."),                     # 192.168.x.x
    re.compile(r"^169\.254\."),                     # link-local
    re.compile(r"^0\."),                            # unspecified
    re.compile(r"^127\.0\.0\.1$"),                   # localhost
]

def is_private_ip(host: str) -> bool:
    """
    Returns True if host matches any known private IP pattern.
    Handles both IPv4 and IPv6 literals.
    """
    # IPv6 private addresses (e.g., fd00::/8)
    if re.match(r"^fd[0-9a-fA-F]{1,3}:", host):
        return True
    # IPv6 loopback ::1
    if host in ("::1", "0:0:0:0:0:0:0:1"):
        return True
    # IPv4 dotted quad
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", host):
        for pattern in PRIVATE_IP_PATTERNS:
            if pattern.match(host):
                return True
    return False

def handle_webhook(webhook_link: str) -> str:
    """
    Validate a webhook URL and return it only if it points to an approved
    public API endpoint. Raises ValueError otherwise.

    Args:
        webhook_link: The URL provided by an external service.

    Returns:
        A safely validated, canonicalized URL string.
    """
    if not webhook_link or not isinstance(webhook_link, str):
        raise ValueError("webhook_link must be a non-empty string")

    parsed = urlparse(webhook_link)

    # Enforce https scheme only
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject private or reserved IP addresses
    if is_private_ip(host):
        raise ValueError(f"URL hostname {host} points to a private or reserved IP")

    # Resolve potential IDNA domains
    try:
        host_ascii = host.encode("idna").decode()
    except Exception as exc:
        raise ValueError(f"Invalid hostname encoding: {exc}") from exc

    # Check against approved domains
    if host_ascii.lower() not in APPROVED_DOMAINS:
        # Allow subdomains of approved domains
        allowed = False
        for domain in APPROVED_DOMAINS:
            if host_ascii.lower().endswith("." + domain):
                allowed = True
                break
        if not allowed:
            raise ValueError(f"Domain {host_ascii} is not approved")

    # Reconstruct the URL to ensure it is canonical
    safe_parts = (
        parsed.scheme,
        host_ascii,          # hostname (ASCII)
        str(parsed.port) if parsed.port else "",
        parsed.path,
        parsed.params,
        parsed.query,
        parsed.fragment,
    )
    safe_url = urlunparse(safe_parts)

    return safe_url