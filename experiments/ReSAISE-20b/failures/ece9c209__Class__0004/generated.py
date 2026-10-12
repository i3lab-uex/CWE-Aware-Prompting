import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of domains considered safe.  Add or remove as needed.
ALLOWED_DOMAINS = {
    "api.example.com",
    "services.trustedpartner.org",
    "v1.secure.api.net",
}

# Regular expression to match IPv4 and IPv6 addresses in the netloc.
IP_RE = re.compile(r"^\[?([0-9a-fA-F:.]+)\]?$")


def _is_private_ip(address: str) -> bool:
    """
    Determine if an IP address string is private, loopback or link-local.
    Raises ValueError if the address cannot be parsed as an IP.
    """
    try:
        ip_obj = ipaddress.ip_address(address)
    except ValueError as exc:
        raise ValueError(f"Invalid IP address: {address}") from exc

    return ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local


def _netloc_is_allowed(netloc: str) -> bool:
    """
    Verify that the netloc is either a permitted domain or a public IP.
    """
    # Remove port if present
    host = netloc.split(":")[0]

    # Check for IP address (IPv4 or IPv6)
    match = IP_RE.match(host)
    if match:
        ip_addr = match.group(1)
        # IPv6 addresses are enclosed in brackets, strip them
        ip_addr = ip_addr.strip("[]")
        if _is_private_ip(ip_addr):
            return False
        # Public IP is allowed only if the entire URL was already validated
        # by other means; for safety we disallow any IP not in the allowed list.
        return False

    # Otherwise host is a domain name – check against the whitelist
    return host.lower() in ALLOWED_DOMAINS


def validate_api_endpoint(api_url: str) -> str:
    """
    Validate that the supplied URL points to a trusted external API endpoint.
    
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
        If the URL is malformed, uses a disallowed domain or attempts to reach an internal network address.
    """
    if not isinstance(api_url, str):
        raise ValueError("api_url must be a string")

    parsed = urlparse(api_url)

    # Ensure we have an absolute URL with scheme and netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute and contain a scheme (e.g., https://)")

    # Only allow HTTPS to mitigate man‑in‑the‑middle attacks
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # Validate netloc against whitelist or reject private IPs
    if not _netloc_is_allowed(parsed.netloc):
        raise ValueError(f"Domain or IP '{parsed.netloc}' is not trusted")

    # Reconstruct the URL to ensure it is normalized
    cleaned = urlunparse(parsed._replace(scheme="https"))
    return cleaned