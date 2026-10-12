import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Pre‑approved public API endpoints (example domains)
PRE_APPROVED_DOMAINS = {
    "api.example.com",
    "service.partner.org",
    "public.api.io",
}

# Regular expression to detect internal or private IP addresses
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:
        (?:10(?:\.\d{1,3}){3})|                    # 10.0.0.0/8
        (?:172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})|  # 172.16.0.0/12
        (?:192\.168(?:\.\d{1,3}){2})|                # 192.168.0.0/16
        (?:127(?:\.\d{1,3}){3})|                    # 127.0.0.0/8
        (?:169\.254(?:\.\d{1,3}){2})|                # 169.254.0.0/16
        (?:::1)                                      # IPv6 loopback
    )$
    """,
    re.VERBOSE,
)


def _is_private_ip(ip_str: str) -> bool:
    """Return True if the given IP string is a private or loopback address."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not a valid IP address
        return False


def _is_internal_host(host: str) -> bool:
    """Check if the host is an internal or private IP address."""
    # Strip port if present
    host = host.split(":")[0]
    # If hostname looks like an IP address
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", host) or re.match(r"^[a-f0-9:]+$", host):
        return _is_private_ip(host)
    # Resolve hostname to IPs if needed (optional, skip for security)
    return False


def process_webhook(webhook_url: str) -> str:
    """
    Validate a webhook URL and return it if it points to an approved public API endpoint.

    Parameters
    ----------
    webhook_url : str
        The URL provided by an external service.

    Returns
    -------
    str
        The validated and canonicalized URL.

    Raises
    ------
    ValueError
        If the URL's domain is not in the pre-approved list or if an internal address is used.
    """
    if not isinstance(webhook_url, str):
        raise ValueError("webhook_url must be a string")

    parsed = urlparse(webhook_url)

    # Scheme check
    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL must use http or https scheme")

    # Netloc (host:port) must be present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain)")

    host = parsed.netloc.split(":")[0].lower()

    # Reject internal addresses
    if _is_internal_host(host):
        raise ValueError("Internal or private IP addresses are not allowed")

    # Domain must be in the whitelist
    if host not in PRE_APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not an approved endpoint")

    # Reconstruct the URL to ensure consistent formatting
    cleaned_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc.lower(),
            parsed.path or "/",
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return cleaned_url