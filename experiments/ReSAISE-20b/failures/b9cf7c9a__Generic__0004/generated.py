import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# A minimal list of approved external API domains.
# In a real application, this should be configurable or derived from a secure source.
APPROVED_DOMAINS = {
    "api.github.com",
    "api.openai.com",
    "api.weather.gov",
    # add more approved domains here
}

# Regex to match private IP ranges that should never be reachable externally.
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:
        (10\.\d{1,3}\.\d{1,3}\.\d{1,3}) |            # 10.0.0.0/8
        (172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}) |# 172.16.0.0/12
        (192\.168\.\d{1,3}\.\d{1,3}) |                # 192.168.0.0/16
        (169\.254\.\d{1,3}\.\d{1,3}) |                # 169.254.0.0/16
        (127\.\d{1,3}\.\d{1,3}\.\d{1,3}) |             # 127.0.0.0/8
        (fc00::|fd00::)/7 |                           # IPv6 ULA
        (::1)                                          # loopback IPv6
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is a private or reserved address."""
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback
    except ValueError:
        return False

def check_api_url(endpoint_url: str) -> str:
    """
    Validate that the given URL points to an approved external API domain
    and does not target any internal or private network addresses.

    Parameters:
        endpoint_url (str): The URL to validate.

    Returns:
        str: The validated, normalized URL.

    Raises:
        ValueError: If the URL is not HTTPS, does not belong to an approved domain,
                    or resolves to a private/internal address.
    """
    # Parse the URL
    parsed = urlparse(endpoint_url)

    if not parsed.scheme or parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed for external API calls.")

    if not parsed.netloc:
        raise ValueError("URL must contain a valid host component.")

    # Normalise the hostname (lowercase, strip trailing dot)
    hostname = parsed.hostname.lower().rstrip('.')
    if hostname not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not on the approved list.")

    # Resolve hostname to IP addresses (basic check, no DNS resolution here)
    # In a real implementation you would resolve the hostname and verify each IP.
    # For demonstration, we check if the hostname itself looks like an IP.
    if re.match(r'^\d{1,3}(\.\d{1,3}){3}$', hostname) or re.match(r'^[0-9a-fA-F:]+$', hostname):
        if _is_private_ip(hostname) or PRIVATE_IP_REGEX.match(hostname):
            raise ValueError("URL points to a private/internal IP address.")

    # Reconstruct the URL without any fragment/query if you want strict normalization
    normalized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return normalized

# Example usage (commented out to avoid accidental execution)
# try:
#     url = check_api_url("https://api.github.com/repos/octocat/Hello-World")
#     print(f"Validated URL: {url}")
# except ValueError as e:
#     print(f"Validation failed: {e}")