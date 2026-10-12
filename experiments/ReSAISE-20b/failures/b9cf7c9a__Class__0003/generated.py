import re
import socket
from urllib.parse import urlparse, unquote
import ipaddress

# --------------------------------------------------------------------------- #
# Configuration – list of approved domains or domain patterns.
# Add any additional external APIs you trust here.  Patterns can contain
# wildcards (*) to allow sub‑domains, e.g. "api.example.com" or "*.trusted.io".
# --------------------------------------------------------------------------- #
APPROVED_DOMAIN_PATTERNS = [
    r"^api\.example\.com$",      # exact match
    r"^.*\.trusted\.io$",       # any sub‑domain of trusted.io
    r"^https://service\.mycompany\.com$",  # full URL with scheme (optional)
]

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _domain_matches(domain: str) -> bool:
    """
    Check if the given domain matches any approved pattern.
    The patterns are regexes; wildcards '*' are converted to '.*'.
    """
    for pattern in APPROVED_DOMAIN_PATTERNS:
        # Convert a simple wildcard pattern to regex if needed
        regex = re.escape(pattern).replace(r"\*", ".*")
        if re.fullmatch(regex, domain, flags=re.IGNORECASE):
            return True
    return False

def _is_private_ip(ip: str) -> bool:
    """
    Determine if an IP address is private, loopback, or reserved.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_reserved
    except ValueError:
        # Not a valid IP address
        return False

# --------------------------------------------------------------------------- #
# Main validation function
# --------------------------------------------------------------------------- #

def check_api_url(endpoint_url: str) -> str:
    """
    Validate that the supplied URL points to an approved external API.
    
    Parameters
    ----------
    endpoint_url : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it is considered safe.

    Raises
    ------
    ValueError
        If the URL does not resolve to an approved domain, or if it resolves
        to a private/loopback/reserved IP address.
    """
    # 1. Parse the URL
    parsed = urlparse(endpoint_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {endpoint_url}")

    # 2. Ensure scheme is http or https
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # 3. Unquote the netloc (in case of encoded characters)
    host = unquote(parsed.hostname or "")
    if not host:
        raise ValueError(f"URL does not contain a hostname: {endpoint_url}")

    # 4. Check against approved domain patterns
    if not _domain_matches(host):
        raise ValueError(f"Domain '{host}' is not in the approved list")

    # 5. Resolve hostname to IP(s) and ensure none are private/loopback
    try:
        addr_info = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{host}': {exc}") from exc

    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP {ip} for host '{host}' is private or reserved")

    # 6. Return the original URL (unchanged)
    return endpoint_url