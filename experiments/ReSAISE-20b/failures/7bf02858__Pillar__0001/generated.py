import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Approved domains (can be expanded)
APPROVED_DOMAINS = {
    "api.mycompany.com",
    "service.example.org",
}

# Regular expression to detect IPv4 or IPv6 addresses in the netloc
IP_REGEX = re.compile(r"""
    ^\s*
    (?:
        # IPv6 literal
        \[
            (?P<ipv6>[^]]+)
        \]
    |
        # IPv4 literal
        (?P<ipv4>\d{1,3}(?:\.\d{1,3}){3})
    )
    (?::\d+)?   # optional port
    \s*$
""", re.VERBOSE)


def _is_internal_ip(address: str) -> bool:
    """
    Determine if the given IP address string is in a private, loopback,
    or reserved range.
    """
    try:
        ip_obj = ipaddress.ip_address(address)
        return ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved
    except ValueError:
        # Not a valid IP address
        return False


def _extract_host(netloc: str) -> str:
    """
    Extract the host part from a netloc, removing any port.
    Handles IPv6 addresses enclosed in brackets.
    """
    match = IP_REGEX.match(netloc)
    if match:
        # netloc contains an IP literal
        return match.group("ipv6") or match.group("ipv4")
    # otherwise, strip port
    return netloc.split(":")[0]


def process_hook(hook_url: str) -> str:
    """
    Validate the provided webhook URL and return it if it points to an
    approved public-facing API endpoint.

    Parameters
    ----------
    hook_url : str
        The URL received from an external service.

    Returns
    -------
    str
        The original URL if it passes validation.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTPS, points to an unapproved domain,
        or targets a private/internal IP address.
    """
    if not isinstance(hook_url, str):
        raise ValueError("hook_url must be a string")

    parsed = urlparse(hook_url)

    # Ensure HTTPS scheme
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # Extract host (domain or IP)
    host = _extract_host(parsed.netloc)

    # Check if host is an IP address
    if re.match(r"^\d{1,3}(?:\.\d{1,3}){3}$", host) or re.match(r"^[0-9a-fA-F:]+$", host):
        if _is_internal_ip(host):
            raise ValueError("Internal IP addresses are not allowed")
        # For external IPs, no domain whitelist check (but could be added)
    else:
        # Domain name: enforce approved list
        if host.lower() not in {d.lower() for d in APPROVED_DOMAINS}:
            raise ValueError(f"Domain '{host}' is not approved")

    # Reconstruct URL to normalize (e.g., remove duplicate slashes)
    safe_url = urlunparse(parsed)

    return safe_url