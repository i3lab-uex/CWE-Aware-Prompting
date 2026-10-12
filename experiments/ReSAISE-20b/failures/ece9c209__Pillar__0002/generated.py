import ipaddress
from urllib.parse import urlparse, urlunparse

# Whitelisted domains for external API calls
ALLOWED_DOMAINS = {
    "api.example.com",
    "services.trusted.org",
    "data.partner.net",
}

# Private IP networks that should never be reachable
PRIVATE_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),   # localhost
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("::1/128"),      # IPv6 loopback
    ipaddress.ip_network("fc00::/7"),     # Unique local address (ULA)
]

def _is_private_ip(host: str) -> bool:
    """Return True if the host resolves to a private IP address."""
    try:
        # Resolve hostname or treat as numeric IP
        addr = ipaddress.ip_address(host)
    except ValueError:
        # Not a numeric IP, assume it resolves to a public address
        return False

    for net in PRIVATE_NETWORKS:
        if addr in net:
            return True
    return False

def validate_api_endpoint(api_url: str) -> str:
    """
    Validate that the given URL points to an allowed external API endpoint.

    Parameters
    ----------
    api_url : str
        The URL to validate.

    Returns
    -------
    str
        A normalized, validated URL that is safe for external API calls.

    Raises
    ------
    ValueError
        If the URL is not part of the allowed domains or resolves to a private IP.
    """
    parsed = urlparse(api_url)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL scheme must be http or https")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Reject private IP addresses
    if _is_private_ip(hostname):
        raise ValueError("URL resolves to a private IP address")

    # Reject URLs that point to disallowed domains
    if hostname not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not trusted")

    # Reconstruct a clean URL (strip fragment and query if needed)
    safe_url = urlunparse(
        (
            parsed.scheme,
            f"{hostname}{':' + str(parsed.port) if parsed.port else ''}",
            parsed.path or "/",
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return safe_url

# Example usage:
if __name__ == "__main__":
    try:
        print(validate_api_endpoint("https://api.example.com/v1/users"))
    except ValueError as e:
        print(f"Validation failed: {e}")