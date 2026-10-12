import re
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
import socket
import ipaddress

# ------------------------------------------------------------------
# Configuration: approved external API domains
# Add or remove domains as required for your environment.
APPROVED_DOMAINS = {
    "api.openai.com",
    "api.github.com",
    "api.weather.gov",
}

# Regex for detecting private IP ranges
_PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (?:
        # 10.0.0.0/8
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        # 172.16.0.0/12
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        # 192.168.0.0/16
        192\.168\.\d{1,3}\.\d{1,3}|
        # 127.0.0.0/8 (loopback)
        127\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        # IPv6 private ranges
        ::1|fc00:|fd00:
    )
    $
    """,
    re.VERBOSE | re.IGNORECASE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or loopback."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Invalid IP string – treat as non‑private to allow further checks
        return False

def _resolve_hostname(hostname: str) -> list[str]:
    """Return a list of IP addresses for the given hostname."""
    try:
        return socket.gethostbyname_ex(hostname)[2]
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

def check_api_url(endpoint_url: str) -> str:
    """
    Validate that a URL points to an approved external API.

    Parameters
    ----------
    endpoint_url : str
        The URL to validate.

    Returns
    -------
    str
        The normalized URL that has been verified as safe.

    Raises
    ------
    ValueError
        If the URL is not HTTPS, points to an unapproved domain,
        or resolves to a private/internal IP address.
    """
    if not endpoint_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(endpoint_url)

    # 1. Enforce HTTPS scheme
    if parsed.scheme.lower() != "https":
        raise ValueError("Only 'https' URLs are allowed")

    # 2. Ensure hostname is present
    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    # 3. Check against approved domain list (case‑insensitive)
    host = parsed.hostname.lower()
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved")

    # 4. Resolve hostname to IP addresses
    ips = _resolve_hostname(host)

    # 5. Ensure none of the resolved IPs are private or internal
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' for domain '{host}' is private or internal")

    # 6. Re‑build a clean, canonical URL
    cleaned = parsed._replace(
        netloc=f"{parsed.hostname}:{parsed.port}" if parsed.port else parsed.hostname,
        params="",
        query=urllib.parse.urlencode(parse_qs(parsed.query), doseq=True),
        fragment="",
    )
    return urlunparse(cleaned)

# Example usage (comment out in production)
if __name__ == "__main__":
    try:
        safe_url = check_api_url("https://api.openai.com/v1/chat/completions")
        print(f"Validated URL: {safe_url}")
    except ValueError as err:
        print(f"URL validation failed: {err}")