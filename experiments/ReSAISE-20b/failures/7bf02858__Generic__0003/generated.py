import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved public API domains (subdomains allowed)
APPROVED_DOMAINS = {
    "api.example.com",
    "auth.example.org",
    "service.example.net",
}

# Regular expression to detect private IP address ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (?:  # Start of non-capturing group for IP blocks
        (10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        169\.254\.\d{1,3}\.\d{1,3}
    )
    $
    """,
    re.VERBOSE,
)


def _is_private_ip(host: str) -> bool:
    """Return True if host is a private IP address."""
    try:
        # Attempt to interpret as an IP
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        # Not an IP, check regex for special cases like 169.254.x.x
        return bool(PRIVATE_IP_REGEX.match(host))


def _is_approved_domain(domain: str) -> bool:
    """Check if the domain or any of its parent domains are in the approved list."""
    parts = domain.lower().split(".")
    for i in range(len(parts)):
        candidate = ".".join(parts[i:])
        if candidate in APPROVED_DOMAINS:
            return True
    return False


def process_hook(hook_url: str) -> str:
    """
    Validate and sanitize a webhook URL.

    Parameters
    ----------
    hook_url : str
        The raw URL received from an external service.

    Returns
    -------
    str
        A sanitized URL that references an approved public API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is not approved or points to an internal/private network.
    """
    if not hook_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(hook_url)

    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL missing hostname")

    # Reject private or loopback IPs
    if _is_private_ip(host):
        raise ValueError(f"URL host {host} is a private or loopback address")

    # Reject any hostname that isn't in the approved list
    if not _is_approved_domain(host):
        raise ValueError(f"Hostname {host} is not an approved API domain")

    # Rebuild the URL to ensure no query parameters or fragments that could
    # alter the intended endpoint.
    sanitized = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,  # retains port if present
            parsed.path.rstrip("/"),  # normalise trailing slash
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return sanitized


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    try:
        print(process_hook("https://api.example.com/v1/notify?token=abc"))
    except ValueError as e:
        print(f"Validation failed: {e}")