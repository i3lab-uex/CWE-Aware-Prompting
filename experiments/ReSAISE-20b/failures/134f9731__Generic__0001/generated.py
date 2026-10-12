import re
from urllib.parse import urlparse, urlunparse

# Approved public API domains (add as needed)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "service.partner.org",
    "webhooks.secure.net",
}

# Regex to detect private IP ranges (RFC1918 and loopback)
PRIVATE_IP_RE = re.compile(
    r"^(?:(?:10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}"
    r"|192\.168\.\d{1,3}\.\d{1,3})$"
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the string is a private IP address."""
    return bool(PRIVATE_IP_RE.match(ip))


def verify_webhook(webhook_endpoint: str) -> str:
    """
    Validate an external webhook URL and return a sanitized version
    suitable for internal API calls.

    Parameters
    ----------
    webhook_endpoint : str
        External webhook URL to validate.

    Returns
    -------
    str
        A validated, sanitized URL that is safe for internal use.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP/HTTPS, if the domain is not in the whitelist,
        or if it resolves to a private IP address.
    """
    # Parse URL
    parsed = urlparse(webhook_endpoint)

    # Enforce http/https scheme
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http and https are allowed.")

    # Enforce presence of netloc
    if not parsed.netloc:
        raise ValueError("URL must contain a hostname or IP address.")

    # Separate host and port
    host, _, _ = parsed.netloc.partition(":")

    # Reject private IPs (IPv4 only for simplicity)
    if re.match(r"\d+\.\d+\.\d+\.\d+$", host) and _is_private_ip(host):
        raise ValueError("URL resolves to a private IP address, which is disallowed.")

    # Reject hosts that are not in the whitelist
    if host.lower() not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the approved whitelist.")

    # Reconstruct a clean URL (preserve path/query/fragment)
    sanitized = urlunparse(
        (
            parsed.scheme,
            host + (f":{parsed.port}" if parsed.port else ""),
            parsed.path or "/",
            "",  # params
            parsed.query,
            parsed.fragment,
        )
    )

    return sanitized


# Example usage (uncomment to test):
# try:
#     url = verify_webhook("https://api.example.com/webhook?token=abc")
#     print(f"Validated URL: {url}")
# except ValueError as e:
#     print(f"Validation error: {e}")