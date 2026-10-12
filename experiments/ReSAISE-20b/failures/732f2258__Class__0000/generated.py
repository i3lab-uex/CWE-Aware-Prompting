import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# --------------------------------------------------------------------------- #
# Configuration: list of approved public API domains.  Update as needed.
ALLOWED_DOMAINS = {
    "api.example.com",
    "services.allowed.org",
    "gateway.trusted.net"
}

# Regular expression for detecting private IP address patterns.
PRIVATE_IP_RE = re.compile(
    r"^(10\.|172\.(1[6-9]|2\d|3[0-1])\.|192\.168\.)"
)

# --------------------------------------------------------------------------- #
def _is_private_ip(host: str) -> bool:
    """
    Determine whether a hostname or IP address resolves to a private network
    address.  The function attempts an IP lookup; if the host is not an IP,
    it returns False.
    """
    try:
        # Resolve IPv4 and IPv6 addresses
        for ip in ipaddress.ip_address(host).exploded.split(","):
            if isinstance(ip, str) and PRIVATE_IP_RE.match(ip):
                return True
    except ValueError:
        # Not a direct IP; treat as hostname – still safe if not in allowed list
        return False
    return False


def _normalize_url(parsed: "ParseResult") -> str:
    """
    Reconstruct a URL from its parsed components, normalizing scheme and
    removing fragments.  This ensures the returned value is deterministic.
    """
    # Normalize scheme to lowercase
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()

    # Remove default ports
    if scheme == "http" and netloc.endswith(":80"):
        netloc = netloc[:-3]
    elif scheme == "https" and netloc.endswith(":443"):
        netloc = netloc[:-4]

    return urlunparse((scheme, netloc, parsed.path or "", "", "", ""))


def analyze_webhook(webhook_address: str) -> str:
    """
    Validate a webhook URL supplied by an external service and return a
    sanitized, internally‑safe URL that can be used for subsequent API calls.

    Parameters:
        webhook_address (str): The raw URL received from the external service.

    Returns:
        str: A validated and normalized URL that points to an approved domain.

    Raises:
        ValueError: If the domain is not in ALLOWED_DOMAINS or if the URL
                    points to a private/internal network.
    """
    # Parse the incoming URL
    parsed = urlparse(webhook_address)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL: missing scheme or host")

    # Reject URLs that use non‑HTTP/HTTPS schemes
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'")

    # Extract hostname (without port)
    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a valid hostname")

    # 1. Check against private IP ranges
    if _is_private_ip(host):
        raise ValueError("URL points to a private network address")

    # 2. Ensure domain is in the approved list
    if host.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not authorized")

    # 3. Return a normalized URL (strip path, query, fragment)
    return _normalize_url(parsed)


# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
if __name__ == "__main__":
    try:
        safe_url = analyze_webhook("https://api.example.com/webhook?token=abc")
        print(f"Validated URL: {safe_url}")
    except ValueError as e:
        print(f"Validation failed: {e}")