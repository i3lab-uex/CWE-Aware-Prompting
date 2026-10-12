import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved domains for external API calls.
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.partner.org",
    "data.provider.net",
}

# Optional: Allow subdomains of approved domains.
ALLOW_SUBDOMAINS = True


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private, loopback, or link‑local."""
    return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(
        ip
    ).is_loopback or ipaddress.ip_address(ip).is_link_local


def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve the hostname to all IPv4 and IPv6 addresses.
    Returns a list of string IPs. Raises socket.gaierror if resolution fails.
    """
    infos = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    return [sock[4][0] for sock in infos]


def _is_allowed_domain(host: str) -> bool:
    """
    Check if the host is in the whitelist.
    If subdomains are allowed, check that the hostname ends with a whitelisted domain.
    """
    if host in ALLOWED_DOMAINS:
        return True
    if not ALLOW_SUBDOMAINS:
        return False

    # Normalize host: strip trailing dot if present
    host = host.rstrip(".")
    for domain in ALLOWED_DOMAINS:
        if host == domain or host.endswith("." + domain):
            return True
    return False


def check_api_url(endpoint_url: str) -> str:
    """
    Validate that an external API URL points to an approved domain and does not
    resolve to any internal/private IP address.

    Args:
        endpoint_url: The URL string to validate.

    Returns:
        A normalized, validated URL string.

    Raises:
        ValueError: If the URL is not HTTPS, uses an unapproved domain,
                    resolves to a private IP, or cannot be resolved.
    """
    if not endpoint_url:
        raise ValueError("URL must not be empty")

    parsed = urlparse(endpoint_url)

    # Ensure scheme is HTTPS (or HTTP if explicitly allowed)
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed for external APIs")

    # Ensure host is present
    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    host = parsed.hostname.lower()

    # Check against the whitelist
    if not _is_allowed_domain(host):
        raise ValueError(f"Domain '{host}' is not in the approved list")

    # Resolve hostname to IPs and check for private addresses
    try:
        resolved_ips = _resolve_hostname(host)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{host}': {exc}") from exc

    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(
                f"Hostname '{host}' resolves to a private IP address ({ip})"
            )

    # Rebuild the URL to ensure consistency (e.g., remove default ports)
    cleaned = parsed._replace(
        netloc=host if not parsed.port else f"{host}:{parsed.port}",
        scheme="https",
    )
    return urlunparse(cleaned)