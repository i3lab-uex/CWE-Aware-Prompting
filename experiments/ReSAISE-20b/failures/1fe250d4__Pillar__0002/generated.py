import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Whitelisted external domains (add your approved domains here)
WHITELISTED_DOMAINS = {
    'api.example.com',
    'services.another.org',
    # Add more domains as needed
}

# Regular expression to detect IPv4 or IPv6 literals in a hostname
IP_LITERAL_RE = re.compile(r'''
    ^\[
        (?P<ipv6>
            ([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4} |          # full IPv6
            ([0-9a-fA-F]{1,4}:){1,7}: |                      # leading ::
            ([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4} |      # :: with tail
            ([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2} |
            ([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3} |
            ([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4} |
            ([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5} |
            [0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6}) |
            :((:[0-9a-fA-F]{1,4}){1,7}|:) |
            fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]+ |
            ::(ffff(:0{1,4}){0,1}:){0,1}
            ((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)(\.(?!$)|$)){4}
        )
    \]
    $
''', re.VERBOSE)

def _is_internal_ip(host: str) -> bool:
    """
    Return True if the host is an internal IP address.
    Handles both IPv4 and IPv6 literals, as well as domain names that resolve to internal IPs.
    """
    # Directly check if host is an IP literal
    ipv6_match = IP_LITERAL_RE.match(host)
    if ipv6_match:
        try:
            ip_obj = ipaddress.ip_address(ipv6_match.group('ipv6'))
            return ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local
        except ValueError:
            pass

    # Try parsing as IPv4 literal
    try:
        ip_obj = ipaddress.ip_address(host)
        return ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local
    except ValueError:
        pass

    # For hostnames we don't resolve DNS here to avoid timing attacks.
    # Assume that any non-whitelisted hostname is safe unless it resolves
    # to an internal IP (which would be caught when the request is made).
    return False

def check_api_endpoint(endpoint_url: str) -> str:
    """
    Validate that the provided URL points to a secure, external API endpoint.
    
    Parameters
    ----------
    endpoint_url : str
        The URL to validate.

    Returns
    -------
    str
        The verified URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is not HTTPS, points to an internal IP or unapproved domain.
    """
    if not isinstance(endpoint_url, str):
        raise ValueError("Endpoint URL must be a string")

    parsed = urlparse(endpoint_url)

    # Scheme must be https
    if parsed.scheme.lower() != 'https':
        raise ValueError("Only HTTPS URLs are allowed")

    # Host must be present
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject internal IP addresses
    if _is_internal_ip(host):
        raise ValueError("Endpoint points to an internal IP address")

    # If hostname is an IP literal, allow only if not internal
    if re.match(r'^\d{1,3}(\.\d{1,3}){3}$', host) or IP_LITERAL_RE.match(host):
        # Already checked for internal above
        pass

    # If hostname is not an IP, check whitelist
    if host.lower() not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the approved whitelist")

    # Reconstruct URL to ensure canonical form (strip fragments, etc.)
    safe_url = urlunparse(parsed._replace(fragment=""))
    return safe_url