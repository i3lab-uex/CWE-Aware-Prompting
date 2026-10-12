import re
from urllib.parse import urlparse, urlunparse, ParseResult
import socket
import ipaddress

# --------------------------------------------------------------------------- #
# Whitelist of approved public API endpoints (scheme, host)
# --------------------------------------------------------------------------- #
WHITELIST = {
    ("https", "api.example.com"),
    ("https", "services.mycorp.org"),
    ("http",  "public.api.net"),
}

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (
        10\.           # 10.0.0.0/8
      | 172\.(1[6-9]|2\d|3[0-1])\.   # 172.16.0.0/12
      | 192\.168\.
    )
    \d{1,3}\.\d{1,3}$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private/reserved range."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address (e.g., hostname)
        return False

def _resolve_host(host: str) -> list[str]:
    """
    Resolve a hostname to its IPv4 addresses.
    Returns a list of string IPs. Raises socket.gaierror if resolution fails.
    """
    try:
        # getaddrinfo may return multiple families; we filter for IPv4 only
        infos = socket.getaddrinfo(host, None, socket.AF_INET)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{host}': {exc}") from exc

    return [info[4][0] for info in infos]

def validate_callback(callback_url: str) -> str:
    """
    Validate an external webhook URL and return a sanitized, secure URL
    that can be used for internal API calls.

    Parameters
    ----------
    callback_url : str
        The external webhook URL to validate.

    Returns
    -------
    str
        A validated, safe URL that is allowed for internal API interactions.

    Raises
    ------
    ValueError
        If the URL domain is not from the approved API endpoint list,
        or if it resolves to an internal/private IP address.
    """
    # 1. Parse the URL
    parsed = urlparse(callback_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: '{callback_url}'")

    # 2. Check against whitelist
    host = parsed.hostname.lower()
    key = (parsed.scheme, host)
    if key not in WHITELIST:
        raise ValueError(f"Domain '{host}' is not whitelisted")

    # 3. Resolve hostname and ensure no private IPs
    ips = _resolve_host(host)
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{host}' resolves to private IP {ip}")

    # 4. Reconstruct a canonical URL (strip fragments, normalize path)
    cleaned = ParseResult(
        scheme=parsed.scheme,
        netloc=f"{host}:{parsed.port}" if parsed.port else host,
        path=parsed.path or "/",
        params="",
        query=parsed.query,
        fragment=""
    )
    return urlunparse(cleaned)

# --------------------------------------------------------------------------- #
# Example usage (for local testing only, remove in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/webhook",
        "http://public.api.net:80/callback?token=abc123",
        "https://evil.com/hack",  # Should raise
    ]

    for url in test_urls:
        try:
            safe_url = validate_callback(url)
            print(f"Validated: {safe_url}")
        except ValueError as e:
            print(f"Rejected '{url}': {e}")