import re
from urllib.parse import urlparse, urlunparse

# Define a whitelist of approved public API domains
WHITELISTED_DOMAINS = {
    "api.example.com",
    "public.service.org",
    "data.provider.net",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_RE = re.compile(
    r"""
    ^(                      # start of string
        10\.                # 10.x.x.x
      | 192\.168\.          # 192.168.x.x
      | 172\.(1[6-9]|2\d|3[0-1])\.   # 172.16-31.x.x
      | 127\..*            # localhost
      | ::1                # IPv6 loopback
    )$
    """,
    re.VERBOSE,
)


def _is_private_ip(ip: str) -> bool:
    """
    Return True if the given IP string is a private address.
    Handles both IPv4 and IPv6.
    """
    if PRIVATE_IP_RE.match(ip):
        return True
    # For IPv4 addresses that do not match the regex, perform a numeric check
    try:
        parts = ip.split(".")
        if len(parts) == 4 and all(0 <= int(p) <= 255 for p in parts):
            first, second = int(parts[0]), int(parts[1])
            if first == 10:
                return True
            if first == 172 and 16 <= second <= 31:
                return True
            if first == 192 and second == 168:
                return True
    except Exception:
        pass
    return False


def verify_webhook(webhook_endpoint: str) -> str:
    """
    Validate that the given webhook URL points to an approved public API endpoint.
    Raises ValueError if validation fails.

    Parameters
    ----------
    webhook_endpoint : str
        The external webhook URL to validate.

    Returns
    -------
    str
        A sanitized and validated URL suitable for internal API calls.
    """
    if not isinstance(webhook_endpoint, str):
        raise ValueError("webhook_endpoint must be a string")

    parsed = urlparse(webhook_endpoint)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL scheme must be http or https")

    # Validate host is present
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Reject private IPs
    if _is_private_ip(parsed.hostname):
        raise ValueError("URL points to a private network address")

    # Check against whitelist
    if parsed.hostname.lower() not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{parsed.hostname}' is not whitelisted")

    # Reconstruct a clean URL (strip fragment, ensure path ends with / if empty)
    cleaned_path = parsed.path or "/"
    sanitized = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            cleaned_path,
            "",  # params
            parsed.query,  # keep query parameters
            "",  # fragment removed
        )
    )

    return sanitized