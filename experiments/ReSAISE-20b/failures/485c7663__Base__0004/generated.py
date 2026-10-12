import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of domains that are considered safe. Extend as needed.
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.mycompany.org",
    "public.api.net",
}

# Regular expression to match IPv4 and IPv6 addresses.
IP_REGEX = re.compile(
    r"""
    ^
    (?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
      |
        # IPv6
        \[?[0-9a-fA-F:]+\]?
    )
    $
    """,
    re.VERBOSE,
)


def _is_private_ip(ip: str) -> bool:
    """
    Return True if the given IP address is private, loopback,
    or otherwise non-public.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return not addr.is_global
    except ValueError:
        # Not a valid IP address
        return False


def _resolve_domain(domain: str) -> list[str]:
    """
    Resolve the domain to a list of IP addresses (IPv4 and IPv6).
    Raises socket.gaierror if the domain cannot be resolved.
    """
    return [
        result[4][0]
        for result in socket.getaddrinfo(domain, None, proto=socket.IPPROTO_TCP)
    ]


def enforce_api_security(api_endpoint: str) -> str:
    """
    Verify that the supplied URL points to a safe, external API endpoint.

    The function performs the following checks:

    1. Scheme must be HTTPS.
    2. Domain must be in the ALLOWED_DOMAINS list.
    3. DNS resolution of the domain must yield only public IP addresses.
       Private or unroutable IPs cause a ValueError.
    4. The URL is normalised (e.g., trailing slashes are removed).

    Parameters
    ----------
    api_endpoint : str
        The URL that needs to be verified.

    Returns
    -------
    str
        The verified, normalised URL if it is allowed.

    Raises
    ------
    ValueError
        If the URL targets an unapproved domain, uses a non-HTTPS scheme,
        or resolves to a private/internal IP address.
    """
    if not isinstance(api_endpoint, str):
        raise ValueError("api_endpoint must be a string")

    # Parse the URL
    parsed = urlparse(api_endpoint)

    # 1. Scheme must be HTTPS
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # 2. Domain must be in the approved list
    domain = parsed.hostname
    if not domain:
        raise ValueError("URL must contain a hostname")

    # Reject IP addresses as hostnames
    if IP_REGEX.match(domain):
        raise ValueError("IP addresses are not allowed as hostnames")

    if domain.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not in the list of approved domains")

    # 3. Resolve DNS and check that all IPs are public
    try:
        resolved_ips = _resolve_domain(domain)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve domain '{domain}': {exc}") from exc

    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(
                f"Domain '{domain}' resolves to private IP address {ip}"
            )

    # 4. Normalise the URL (remove default port, trailing slash)
    netloc = domain
    if parsed.port:
        # Keep the port only if it's non-standard (HTTPS default is 443)
        if parsed.port != 443:
            netloc = f"{domain}:{parsed.port}"
    path = parsed.path.rstrip("/")
    normalized = urlunparse(
        (
            "https",
            netloc,
            path,
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return normalized