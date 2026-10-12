import re
from urllib.parse import urlparse, urlunparse

# List of domains that are considered trusted for external API calls.
TRUSTED_DOMAINS = {
    "api.github.com",
    "api.openweathermap.org",
    "api.stripe.com",
    # Add more trusted domains here
}

# Regular expression to detect private/reserved IP addresses.
PRIVATE_IP_RE = re.compile(
    r"""
    ^(?:                                   # start of string
        (?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}) |       # 10.0.0.0/8
        (?:172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}) |  # 172.16.0.0/12
        (?:192\.168\.\d{1,3}\.\d{1,3}) |          # 192.168.0.0/16
        (?:169\.254\.\d{1,3}\.\d{1,3}) |          # 169.254.0.0/16 (link local)
        (?:127\.\d{1,3}\.\d{1,3}\.\d{1,3}) |       # 127.0.0.0/8 (loopback)
        (?:0\.0\.0\.0) |                          # 0.0.0.0
        (?:255\.255\.255\.255)                    # 255.255.255.255
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(host: str) -> bool:
    """Return True if the host is a private or reserved IP address."""
    return PRIVATE_IP_RE.match(host) is not None

def _is_trusted_domain(host: str) -> bool:
    """Return True if the host is in the trusted domain list."""
    # Normalize the host: strip trailing dots and lower case
    host = host.rstrip(".").lower()
    return host in TRUSTED_DOMAINS

def check_api_link(api_link: str) -> str:
    """
    Validate that `api_link` points to an external, trusted API.

    Parameters
    ----------
    api_link : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it is considered safe.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, points to a private IP,
        or is not in the list of trusted domains.
    """
    if not isinstance(api_link, str):
        raise ValueError("api_link must be a string")

    parsed = urlparse(api_link)

    # Ensure scheme is http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Ensure host is present
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Reject private or reserved IP addresses
    if _is_private_ip(parsed.hostname):
        raise ValueError("URL points to a private or reserved IP address")

    # Reject trusted domain if not in whitelist
    if not _is_trusted_domain(parsed.hostname):
        raise ValueError(f"Hostname '{parsed.hostname}' is not in the trusted domain list")

    # Reconstruct URL to ensure it is normalized
    safe_url = urlunparse(parsed._replace(path=parsed.path or "/", params="", query=""))
    return safe_url