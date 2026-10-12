import re
from urllib.parse import urlparse, unquote

# Whitelisted domains and domain patterns (regular expressions)
WHITELISTED_DOMAINS = {
    "api.github.com",
    "api.openweathermap.org",
    "api.weather.gov",
}

# Patterns for internal IP ranges (RFC1918, loopback, link-local)
INTERNAL_IP_PATTERNS = [
    re.compile(r"^10\."),
    re.compile(r"^192\.168\."),
    re.compile(r"^172\.(1[6-9]|2\d|3[0-1])\."),
    re.compile(r"^127\."),
    re.compile(r"^169\.254\."),
]

# Optional: allow specific subdomains or TLDs
WHITELISTED_REGEX = [
    re.compile(r"^api\.example\.com$"),
    re.compile(r"^services\.\w+\.org$"),
]


def _is_internal_ip(host: str) -> bool:
    """
    Check if the host matches any known internal IP pattern.
    The function also accepts IPv6 loopback addresses (::1).
    """
    # Handle numeric IPs
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", host):
        for pattern in INTERNAL_IP_PATTERNS:
            if pattern.match(host):
                return True
    # IPv6 loopback
    if host in ("::1", "0:0:0:0:0:0:0:1"):
        return True
    return False


def _is_whitelisted_domain(host: str) -> bool:
    """
    Validate host against the whitelist. Accept exact matches or regex patterns.
    """
    if host in WHITELISTED_DOMAINS:
        return True
    for pattern in WHITELISTED_REGEX:
        if pattern.match(host):
            return True
    return False


def check_api_url(endpoint_url: str) -> str:
    """
    Validate that the supplied URL points to an approved external API.

    Parameters
    ----------
    endpoint_url : str
        The URL to validate.

    Returns
    -------
    str
        The validated URL (unchanged).

    Raises
    ------
    ValueError
        If the URL is malformed, points to an internal address,
        or does not belong to a whitelisted domain.
    """
    if not endpoint_url:
        raise ValueError("URL must be a non-empty string")

    # Parse the URL
    parsed = urlparse(endpoint_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {endpoint_url}")

    # Normalise the host (lowercase, remove port)
    host = parsed.hostname.lower() if parsed.hostname else ""
    if not host:
        raise ValueError(f"URL missing hostname: {endpoint_url}")

    # Reject internal IP addresses
    if _is_internal_ip(host):
        raise ValueError(f"URL points to an internal IP address: {endpoint_url}")

    # Reject localhost or other non-public hosts
    if host in ("localhost", "127.0.0.1"):
        raise ValueError(f"URL points to a local host: {endpoint_url}")

    # Ensure the domain is whitelisted
    if not _is_whitelisted_domain(host):
        raise ValueError(f"Domain '{host}' is not whitelisted")

    # Optional: further checks (e.g., disallow certain paths or query parameters)
    # For now, we simply return the original URL.

    return endpoint_url