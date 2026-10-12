import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# --------------------------------------------------------------------------- #
# Configuration: List of approved public API domains.
# Add or remove domains as required by your environment.
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.mycompany.org",
    "public.api.service.net",
}

# Regular expression to match IPv4 and IPv6 addresses.
IPV4_RE = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
IPV6_RE = re.compile(r"^\[?[0-9a-fA-F:]+\]?$")

# --------------------------------------------------------------------------- #
def _is_private_ip(hostname: str) -> bool:
    """
    Return True if the hostname resolves to a private IP address.
    Handles both IPv4 and IPv6 literals. If the host is not an IP
    literal, assume it is a public hostname (the caller should
    ensure DNS resolution is safe).
    """
    # IPv4 literal check
    if IPV4_RE.match(hostname):
        try:
            ip = ipaddress.IPv4Address(hostname)
            return ip.is_private
        except ValueError:
            pass

    # IPv6 literal check (may be wrapped in brackets)
    cleaned = hostname.strip("[]")
    if IPV6_RE.match(cleaned):
        try:
            ip = ipaddress.IPv6Address(cleaned)
            return ip.is_private
        except ValueError:
            pass

    # Not an IP literal – treat as public for this check
    return False


def handle_webhook_request(external_url: str) -> str:
    """
    Validate an external webhook URL and return a safe internal API URL.

    Parameters
    ----------
    external_url : str
        The URL supplied by an external service.

    Returns
    -------
    str
        A validated URL that can be safely used for internal API requests.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a private IP address, or its domain is not in the
        list of allowed public API domains.
    """
    # Parse the URL and perform basic validation
    parsed = urlparse(external_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {external_url}")

    # Allow only HTTP/HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}' in URL: {external_url}")

    # Ensure the host is not a private IP address
    hostname = parsed.hostname  # already lower‑cased by urlparse
    if hostname is None:
        raise ValueError(f"URL does not contain a valid host: {external_url}")

    if _is_private_ip(hostname):
        raise ValueError(f"URL points to a private IP address: {external_url}")

    # Validate domain against the allowed list
    if hostname.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not in the list of allowed API domains")

    # Reconstruct the URL to ensure consistency (strip default ports, etc.)
    safe_url = urlunparse(parsed._replace(scheme=parsed.scheme.lower()))
    return safe_url