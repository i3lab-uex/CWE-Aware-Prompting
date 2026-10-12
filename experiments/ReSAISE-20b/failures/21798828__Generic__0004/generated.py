import urllib.parse
import ipaddress

# List of approved API hostnames or IP addresses.
APPROVED_HOSTS = {
    "api.example.com",
    "internal.api.company.local",  # example internal domain
}

# Optional: allow certain IP ranges (e.g., private subnets) if they map to approved hosts.
APPROVED_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("192.168.0.0/16"),
]

def _is_public_host(host: str) -> bool:
    """
    Check if the host is in the approved list or resolves to an allowed IP range.
    """
    # Normalise host (lowercase, strip trailing dot)
    host = host.lower().rstrip(".")
    if host in APPROVED_HOSTS:
        return True

    # Try to interpret as an IP address
    try:
        ip = ipaddress.ip_address(host)
        for net in APPROVED_IP_RANGES:
            if ip in net:
                return True
    except ValueError:
        # Not a direct IP; attempt to resolve if needed (not recommended in production)
        pass

    return False


def handle_webhook(webhook_link: str) -> str:
    """
    Validate a webhook URL and ensure it points to an approved internal API endpoint.

    Parameters
    ----------
    webhook_link : str
        The URL provided by an external service that should trigger an internal API call.

    Returns
    -------
    str
        The original URL if it is considered safe and approved.

    Raises
    ------
    ValueError
        If the URL's domain is not in the approved list or points to a private/internal network location.
    """
    if not webhook_link:
        raise ValueError("Webhook link must be a non-empty string")

    parsed = urllib.parse.urlparse(webhook_link)

    # Basic scheme check
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate host
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    if not _is_public_host(parsed.hostname):
        raise ValueError(f"Hostname '{parsed.hostname}' is not approved")

    # Ensure no userinfo (username/password) in the URL
    if parsed.username or parsed.password:
        raise ValueError("URL must not contain user credentials")

    # Reconstruct the URL to normalise it (e.g., remove default ports)
    cleaned = urllib.parse.urlunparse((
        parsed.scheme,
        f"{parsed.hostname}:{parsed.port}" if parsed.port else parsed.hostname,
        parsed.path or "/",
        "",  # params
        parsed.query,
        ""   # fragment
    ))

    return cleaned