import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of domains considered trustworthy for external API calls.
TRUSTED_DOMAINS = {
    "api.example.com",
    "service.partner.org",
    "data.external.net",
}

# Regular expression for IPv4 and IPv6 literal addresses.
IP_LITERAL_RE = re.compile(r"^\[?(?P<ip>[^:\[\]]+)\]?$")


def _is_private_ip(ip: str) -> bool:
    """
    Determine if the given IP address string is private, loopback,
    or otherwise internal.
    """
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False  # Not a valid IP address
    return (
        addr.is_private or
        addr.is_loopback or
        addr.is_link_local or
        addr.is_reserved or
        addr.is_multicast
    )


def _is_trusted_domain(host: str) -> bool:
    """
    Verify that the hostname is in the list of trusted domains.
    Subdomains are also considered valid if their base domain matches
    one in the TRUSTED_DOMAINS set.
    """
    # Normalize to lowercase for comparison
    host = host.lower()
    # Strip trailing dot (fully qualified domain name)
    if host.endswith("."):
        host = host[:-1]
    # Direct match
    if host in TRUSTED_DOMAINS:
        return True
    # Subdomain check: ensure the suffix matches a trusted domain
    for domain in TRUSTED_DOMAINS:
        if host.endswith("." + domain):
            return True
    return False


def check_api_link(api_link: str) -> str:
    """
    Validate that the provided API URL points to an external, trusted
    endpoint and does not resolve to any internal or sensitive network
    location.

    Parameters:
        api_link (str): The URL to validate.

    Returns:
        str: The normalized, validated URL.

    Raises:
        ValueError: If the URL is not trusted or attempts to access
                    internal networks.
    """
    # Parse and normalize the URL
    parsed = urlparse(api_link)

    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only http and https schemes are allowed")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Check for literal IP addresses in the host part
    match = IP_LITERAL_RE.match(host)
    if match:
        ip_str = match.group("ip")
        if _is_private_ip(ip_str):
            raise ValueError(f"IP address {ip_str} is not allowed (private/internal)")
    else:
        # For domain names, ensure they are in the trusted list
        if not _is_trusted_domain(host):
            raise ValueError(f"Domain '{host}' is not in the list of trusted domains")

    # Reconstruct a clean URL (removes user info, fragments)
    cleaned = parsed._replace(fragment="", username=None, password=None)
    return urlunparse(cleaned)

# Example usage:
if __name__ == "__main__":
    try:
        url = check_api_link("https://api.example.com/v1/data")
        print(f"Validated URL: {url}")
    except ValueError as e:
        print(f"Invalid API link: {e}")