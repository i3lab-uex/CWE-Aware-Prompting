import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Regular expression to detect common internal hostnames
_INTERNAL_HOSTNAME_REGEX = re.compile(
    r'^(?:localhost|127\.0\.0\.1|::1)$', re.IGNORECASE
)

# List of IP networks that are considered internal or non‑public.
_INTERNAL_IP_NETWORKS = [
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('169.254.0.0/16'),  # Link‑local
    ipaddress.ip_network('127.0.0.0/8'),     # Loopback
    ipaddress.ip_network('::1/128'),        # IPv6 loopback
    ipaddress.ip_network('fe80::/10'),      # Link‑local IPv6
]

def _is_internal_ip(ip_str: str) -> bool:
    """Return True if the given IP address string is in a private or
    non‑public network range."""
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        # Not a valid IP address
        return False

    for net in _INTERNAL_IP_NETWORKS:
        if ip in net:
            return True
    return False

def _is_internal_hostname(hostname: str) -> bool:
    """Return True if the hostname resolves to an internal IP or is a
    reserved name such as localhost."""
    # Fast check for obvious names
    if _INTERNAL_HOSTNAME_REGEX.match(hostname):
        return True

    # Resolve the hostname to IPs and check each
    try:
        for ip_str in socket.gethostbyname_ex(hostname)[2]:
            if _is_internal_ip(ip_str):
                return True
    except Exception:
        # If resolution fails we conservatively assume it's not internal
        pass

    return False


def verify_api_address(endpoint_address: str) -> str:
    """
    Validate that `endpoint_address` is a secure, external API endpoint.

    The function performs the following checks:
      * URL scheme must be HTTPS.
      * Hostname cannot resolve to a private or non‑public IP address.
      * Hostname cannot be localhost or any other reserved internal name.
      * URL must not contain a userinfo component (username/password).
      * The returned value is the normalized, verified URL.

    Raises:
        ValueError: If any of the checks fail.
    """
    parsed = urlparse(endpoint_address)

    # Scheme must be https
    if parsed.scheme.lower() != 'https':
        raise ValueError('Only HTTPS URLs are allowed.')

    # No userinfo
    if parsed.username or parsed.password:
        raise ValueError('URL must not contain credentials.')

    # Host cannot be empty
    if not parsed.hostname:
        raise ValueError('URL must contain a hostname.')

    # Reject internal hostnames
    if _is_internal_hostname(parsed.hostname):
        raise ValueError(f'Hostname {parsed.hostname!r} is not allowed.')

    # Reject URLs that resolve to private IPs
    try:
        ips = socket.gethostbyname_ex(parsed.hostname)[2]
        if any(_is_internal_ip(ip) for ip in ips):
            raise ValueError(f'Hostname {parsed.hostname!r} resolves to an internal IP.')
    except Exception as exc:
        raise ValueError(f'Could not resolve hostname {parsed.hostname!r}: {exc}')

    # Rebuild URL to ensure consistent formatting
    verified_url = urlunparse(parsed._replace(fragment=''))
    return verified_url