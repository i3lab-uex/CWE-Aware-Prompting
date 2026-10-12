import re
from urllib.parse import urlparse, urlunparse

# List of approved public API hostnames (case‑insensitive)
APPROVED_HOSTS = {
    "api.example.com",
    "service.mycompany.org",
    "public.api.partner.net",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (
        # 10.0.0.0 – 10.255.255.255
        (10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 172.16.0.0 – 172.31.255.255
        (172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|
        # 192.168.0.0 – 192.168.255.255
        (192\.168\.\d{1,3}\.\d{1,3})|
        # 127.0.0.0 – 127.255.255.255
        (127\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # ::1 (IPv6 loopback)
        (::1) |
        # IPv6 private ranges
        ([0-9a-fA-F]{0,4}:){2,7}([0-9a-fA-F]{0,4})?
    )
    $
    """,
    re.VERBOSE,
)

def is_private_ip(host: str) -> bool:
    """Return True if the host string represents a private IP address."""
    return bool(PRIVATE_IP_RE.match(host))

def normalize_host(host: str) -> str:
    """Return the host in lower‑case, without trailing dot."""
    return host.lower().rstrip(".")

def manage_webhook(url_hook: str) -> str:
    """
    Validate a webhook URL and return it if it points to an approved API endpoint.

    Parameters
    ----------
    url_hook : str
        The URL provided by an external service.

    Returns
    -------
    str
        The validated and normalized URL that references an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is outside the list of approved API endpoints,
        or if it resolves to an internal network location.
    """
    if not isinstance(url_hook, str):
        raise ValueError("url_hook must be a string")

    parsed = urlparse(url_hook)

    # Basic scheme check
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = normalize_host(parsed.hostname or "")
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject private IP addresses or internal hostnames
    if is_private_ip(host) or re.match(r"^localhost\b", host):
        raise ValueError("URL points to an internal network location")

    # Check against approved hosts
    if host not in APPROVED_HOSTS:
        raise ValueError(f"Hostname '{host}' is not an approved endpoint")

    # Re‑build the URL to ensure it uses a normalized form
    cleaned = parsed._replace(netloc=host)
    return urlunparse(cleaned)

# Example usage (for illustration; remove or comment out in production)
if __name__ == "__main__":
    try:
        safe_url = manage_webhook("https://api.example.com/webhooks/123")
        print(f"Safe URL: {safe_url}")
    except ValueError as exc:
        print(f"Invalid webhook: {exc}")