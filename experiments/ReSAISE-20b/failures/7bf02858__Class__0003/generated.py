import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# List of approved API domain patterns (exact match or wildcard subdomains)
APPROVED_DOMAINS = [
    r'^api\.example\.com$',
    r'^.*\.internal\.example\.com$',  # allow subdomains of internal.example.com
    r'^service\.trusted\.org$',
]

# Regular expression for allowed schemes
ALLOWED_SCHEMES = {'http', 'https'}


def _is_approved_domain(domain: str) -> bool:
    """Return True if the domain matches one of the approved patterns."""
    return any(re.match(pattern, domain, re.IGNORECASE) for pattern in APPROVED_DOMAINS)


def _is_internal_ip(ip: str) -> bool:
    """Return True if the IP address is in a private, loopback, link-local,
    or reserved range defined by RFC 1918 / IETF."""
    try:
        addr = ipaddress.ip_address(ip)
        return (
            addr.is_private
            or addr.is_loopback
            or addr.is_link_local
            or addr.is_reserved
        )
    except ValueError:
        # Not a valid IP address (e.g., domain name)
        return False


def _resolve_and_check(domain: str) -> None:
    """Resolve the domain to IPs and ensure none are internal."""
    try:
        # gethostbyname_ex returns (hostname, aliaslist, ipaddrlist)
        _, _, ip_list = socket.gethostbyname_ex(domain)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve domain '{domain}': {exc}") from None

    for ip in ip_list:
        if _is_internal_ip(ip):
            raise ValueError(f"Domain '{domain}' resolves to internal IP {ip}")


def process_hook(hook_url: str) -> str:
    """
    Validate a webhook URL and return a sanitized version that references
    an approved API endpoint.

    Parameters:
        hook_url (str): The URL provided by the external service.

    Returns:
        str: A validated, canonical URL that can safely be used to call an
             internal API.

    Raises:
        ValueError: If the URL uses an unsupported scheme, references a domain
                    outside the approved list, or resolves to an internal IP.
    """
    if not hook_url:
        raise ValueError("hook_url must be a non-empty string")

    parsed = urlparse(hook_url)

    # Scheme check
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http/https are allowed.")

    # Domain (netloc) extraction and validation
    domain = parsed.hostname
    if not domain:
        raise ValueError("URL must contain a valid hostname")

    if not _is_approved_domain(domain):
        raise ValueError(f"Domain '{domain}' is not in the list of approved endpoints")

    # Resolve domain to IPs and ensure none are internal
    _resolve_and_check(domain)

    # Reconstruct the URL to remove any user info or fragments that could
    # cause confusion.  We keep path, params, query, and fragment if present.
    safe_netloc = domain
    if parsed.port:
        safe_netloc += f":{parsed.port}"

    sanitized = urlunparse((
        parsed.scheme.lower(),
        safe_netloc,
        parsed.path or '',
        parsed.params or '',
        parsed.query or '',
        parsed.fragment or ''
    ))

    return sanitized