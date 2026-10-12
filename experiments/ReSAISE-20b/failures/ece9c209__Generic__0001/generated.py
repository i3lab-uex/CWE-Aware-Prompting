import re
from urllib.parse import urlparse, ParseResult

# List of fully‑qualified domain names that are considered trusted.
ALLOWED_DOMAINS = {
    "api.example.com",
    "trusted.api.org",
    # Add additional trusted domains here.
}

# Regular expressions for detecting private or local IP addresses.
PRIVATE_IP_REGEXES = [
    re.compile(r"^127\."),                    # 127.0.0.0/8
    re.compile(r"^10\."),                     # 10.0.0.0/8
    re.compile(r"^172\.(1[6-9]|2[0-9]|3[01])\.") ,  # 172.16.0.0/12
    re.compile(r"^192\.168\."),               # 192.168.0.0/16
    re.compile(r"^::1$"),                     # IPv6 loopback
    re.compile(r"^fe80:"),                    # Link‑local IPv6
]

def _is_private_ip(host: str) -> bool:
    """Return True if the host string looks like a private or local IP."""
    # IPv4
    for regex in PRIVATE_IP_REGEXES:
        if regex.match(host):
            return True
    # IPv6 literals are handled by the same regexes.
    return False

def validate_api_endpoint(api_url: str) -> str:
    """
    Validate that a given URL points to an external, trusted API endpoint.

    Parameters
    ----------
    api_url : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it is considered safe and trusted.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, points to a private/local address,
        or does not belong to one of the allowed domains.
    """
    if not isinstance(api_url, str):
        raise ValueError("api_url must be a string")

    parsed: ParseResult = urlparse(api_url)

    # Scheme must be http or https
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure netloc (host) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc)")

    # Extract host part (may include port)
    host = parsed.hostname
    if not host:
        raise ValueError("Could not determine hostname from URL")

    # Reject localhost or any private IP addresses
    if host.lower() in {"localhost", "127.0.0.1"} or _is_private_ip(host):
        raise ValueError("URL points to a local or private network address")

    # Domain must be in the allowed list
    if host.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not trusted")

    # If all checks pass, return the original URL
    return api_url