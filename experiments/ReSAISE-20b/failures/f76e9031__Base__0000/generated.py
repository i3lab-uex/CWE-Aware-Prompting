import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (case‑insensitive)
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "safe-site.net",
}

# Regex to detect IP addresses (IPv4 & IPv6)
IP_ADDRESS_RE = re.compile(
    r"""
    ^(?:
        (?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})          # IPv4
        |
        \[                                   # IPv6 start
            (?:[0-9a-fA-F]{1,4}:){7}
            [0-9a-fA-F]{1,4}                 # IPv6
        \]                                   # IPv6 end
    )$
    """,
    re.VERBOSE,
)

def _is_ip_address(host: str) -> bool:
    """Return True if host is an IP address (IPv4 or IPv6)."""
    return bool(IP_ADDRESS_RE.match(host))

def _normalize_host(host: str) -> str:
    """
    Convert host to lowercase and strip any trailing dot.
    IPv6 addresses are left as‑is (including brackets).
    """
    host = host.strip().lower()
    if host.endswith("."):
        host = host[:-1]
    return host

def redirect_user_safely(target_url: str) -> str:
    """
    Validate a user‑supplied URL and return it if its domain is approved.

    Parameters
    ----------
    target_url : str
        The URL supplied by the user.

    Returns
    -------
    str
        The original, unmodified URL if it is safe for redirection.

    Raises
    ------
    ValueError
        If the URL's host is not in the approved domain list,
        or if it contains an IP address (which bypasses hostname checks).
    """
    if not target_url:
        raise ValueError("URL must be a non‑empty string")

    parsed = urlparse(target_url)

    # Ensure the URL has a scheme and netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include a scheme (e.g., http://) and host")

    # Reject URLs with non‑HTTP/HTTPS schemes
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Extract host (strip port if present)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject IP addresses outright
    if _is_ip_address(host):
        raise ValueError("IP addresses are not allowed")

    host = _normalize_host(host)

    # Check against approved domains
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Re‑assemble the URL to ensure it hasn't been tampered with
    safe_url = urlunparse(parsed)

    return safe_url

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    try:
        print(redirect_user_safely("https://example.com/path?query=123"))
    except ValueError as e:
        print(f"Invalid URL: {e}")