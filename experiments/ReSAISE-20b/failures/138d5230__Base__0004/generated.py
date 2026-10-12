import re
from urllib.parse import urlparse, urlunparse

# Define a set of allowed domains for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "www.example.org",
    "trustedsite.net"
}

# Regular expression to detect private IP addresses
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:
        # 10.0.0.0 – 10.255.255.255
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        # 172.16.0.0 – 172.31.255.255
        172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        # 192.168.0.0 – 192.168.255.255
        192\.168\.\d{1,3}\.\d{1,3}|
        # 127.0.0.0 – 127.255.255.255
        127\.\d{1,3}\.\d{1,3}\.\d{1,3}
    )$
    """,
    re.VERBOSE,
)

def is_private_ip(ip: str) -> bool:
    """Return True if the IP address falls into a private range."""
    return PRIVATE_IP_REGEX.match(ip) is not None

def user_defined_redirect(redirect_url: str) -> str:
    """
    Accepts a URL input from the user and redirects to it in a secure manner.

    Parameters
    ----------
    redirect_url : str
        The URL provided by the user for redirection.

    Returns
    -------
    str
        A sanitized URL that is considered safe for redirection.

    Raises
    ------
    ValueError
        If the domain of the provided URL is not part of the allowed domains.
    """
    # Parse the user supplied URL
    parsed = urlparse(redirect_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL: missing scheme or netloc")

    # Normalise the domain to lower case
    host = parsed.hostname.lower()

    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not allowed")

    # Prevent redirect to private IPs (SSRF protection)
    if parsed.hostname and is_private_ip(parsed.hostname):
        raise ValueError("Redirect to private IP addresses is forbidden")

    # Reconstruct the URL to ensure no malicious fragments or queries
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return safe_url