import re
import socket
from urllib.parse import urlparse, unquote

# Trusted domains (case‑insensitive)
_TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.reuters.com",
}

# Regular expression to detect private IP ranges
_PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (
        10\.           # 10.0.0.0/8
      | 172\.(1[6-9]|2\d|3[0-1])\.   # 172.16.0.0/12
      | 192\.168\.          # 192.168.0.0/16
      | 127\.\d+\.\d+\.\d+   # loopback
      | 169\.254\.\d+\.\d+   # link local
    )
    \.
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private or reserved range."""
    # IPv4
    try:
        packed = socket.inet_aton(ip)
        return _PRIVATE_IP_RE.match(socket.inet_ntoa(packed)) is not None
    except OSError:
        # Not a valid IPv4 address; ignore for now.
        return False

def _resolve_host(host: str) -> bool:
    """
    Resolve the host to IP addresses and ensure none are private.
    Return True if all resolved IPs are public.
    """
    try:
        # getaddrinfo may return multiple records; we only care about IPv4/IPv6
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return False

    for info in infos:
        ip = info[4][0]
        if _is_private_ip(ip):
            return False
    return True

def validate_feed_url(url: str) -> str:
    """
    Validate that a given RSS feed URL originates from one of the trusted
    providers and does not point to an internal/private network.

    Parameters:
        url (str): The RSS feed URL to validate.

    Returns:
        str: The original URL if it is trusted and safe.

    Raises:
        ValueError: If the URL is malformed, not from a trusted domain,
                    or resolves to an internal/private IP.
    """
    if not isinstance(url, str) or not url.strip():
        raise ValueError("URL must be a non-empty string")

    parsed = urlparse(url.strip())
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP/HTTPS allowed")

    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a valid hostname")

    # Normalize to lowercase for comparison
    host_lower = host.lower()
    if not any(host_lower == domain or host_lower.endswith("." + domain) for domain in _TRUSTED_DOMAINS):
        raise ValueError(f"Domain '{host}' is not in the list of trusted providers")

    # Resolve host and ensure no private IPs
    if not _resolve_host(host):
        raise ValueError(f"Resolved host '{host}' points to a private or internal IP address")

    # Ensure the URL does not contain back‑references that could resolve to
    # internal IPs via DNS tricks. Unquote and strip potential path traversal.
    cleaned_path = unquote(parsed.path)
    if ".." in cleaned_path:
        raise ValueError("URL path contains disallowed traversal sequences")

    # All checks passed; return the original URL
    return url

# Example usage (commented out for module import safety)
# if __name__ == "__main__":
#     test_url = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
#     try:
#         validated = validate_feed_url(test_url)
#         print("Validated URL:", validated)
#     except ValueError as e:
#         print("Validation error:", e)