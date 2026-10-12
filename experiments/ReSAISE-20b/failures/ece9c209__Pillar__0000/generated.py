import re
from urllib.parse import urlparse, unquote
import ipaddress

# List of domains that are considered trusted.
ALLOWED_DOMAINS = {
    "api.example.com",
    "services.trusted.org",
    "data.partner.net",
}

# Regular expression to match IPv4 and IPv6 addresses in a URL.
IP_PATTERN = re.compile(
    r"""
    ^(?P<scheme>https?)://
    (?:
        # IPv4
        (?P<ipv4>(?:\d{1,3}\.){3}\d{1,3})
        |
        # IPv6
        \[
            (?P<ipv6>
                [0-9a-fA-F:.]+
            )
        \]
    )
    (?::(?P<port>\d+))?
    """,
    re.VERBOSE,
)


def _is_internal_ip(address: str) -> bool:
    """
    Return True if the IP address is in a private, loopback or reserved range.
    """
    try:
        ip = ipaddress.ip_address(address)
    except ValueError:
        return False  # Not a valid IP address

    # Exclude private, loopback, link-local, multicast, and unspecified addresses
    return (
        ip.is_private
        or ip.is_loopback
        or ip.is_link_local
        or ip.is_multicast
        or ip.is_unspecified
    )


def validate_api_endpoint(api_url: str) -> str:
    """
    Validate that `api_url` points to a trusted external API endpoint.

    Parameters
    ----------
    api_url : str
        The URL to validate.

    Returns
    -------
    str
        The validated, normalized URL.

    Raises
    ------
    ValueError
        If the URL is not part of an allowed domain or attempts to access
        internal network addresses.
    """
    if not api_url:
        raise ValueError("Empty URL provided")

    # Parse the URL
    parsed = urlparse(api_url)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Resolve any percent-encoded domain
    hostname = unquote(parsed.hostname or "")

    # Check for IP addresses in the hostname part
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", hostname) or re.match(r"^\[.*\]$", hostname):
        # Extract the raw IP string
        ip_str = re.sub(r"^\[|\]$", "", hostname)
        if _is_internal_ip(ip_str):
            raise ValueError("URL resolves to an internal IP address")

    # If hostname is not a plain IP, check against allowed domains
    if hostname and hostname.lower() not in ALLOWED_DOMAINS:
        # Also allow subdomains of allowed domains
        if not any(hostname.lower().endswith("." + domain) for domain in ALLOWED_DOMAINS):
            raise ValueError(f"Domain '{hostname}' is not trusted")

    # Normalize the URL (strip default ports, etc.)
    netloc = parsed.hostname
    if parsed.port:
        # Only include the port if it is non-default for the scheme
        default_port = 443 if parsed.scheme == "https" else 80
        if parsed.port != default_port:
            netloc += f":{parsed.port}"
    normalized = parsed._replace(netloc=netloc).geturl()

    return normalized