import re
import socket
from urllib.parse import urlparse

# ------------------------------------------------------------------
# Approved external API domains (example list – extend as needed)
# ------------------------------------------------------------------
APPROVED_DOMAINS = {
    "api.example.com",
    "service.anotherdomain.org",
    # Add more approved domains here
}

# ------------------------------------------------------------------
# Regular expression to detect private or non‑public IP addresses
# ------------------------------------------------------------------
PRIVATE_IP_RE = re.compile(
    r"""
    (^127\.)|                             # Loopback
    (^10\.)|                               # Class A private
    (^172\.(1[6-9]|2\d|3[0-1])\.)|        # Class B private
    (^192\.168\.)|                         # Class C private
    (^169\.254\.)|                         # Link local
    (^0\.)|                                 # "Non‑existent" network
    (^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$)   # Catch‑all IPv4
    """,
    re.VERBOSE,
)

# ------------------------------------------------------------------
def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is private or otherwise non‑public."""
    return PRIVATE_IP_RE.match(ip) is not None


def validate_service_url(service_url: str) -> str:
    """
    Validate that the supplied URL points to an approved external API.

    Parameters
    ----------
    service_url : str
        The URL string to validate.

    Returns
    -------
    str
        The validated, normalized URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, does not belong to an approved domain,
        or resolves to a private/internal IP address.
    """
    # Parse the URL
    parsed = urlparse(service_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {service_url!r}")

    # Enforce HTTPS (or at least HTTP) – adjust as required
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme {parsed.scheme!r} in URL: {service_url!r}")

    # Normalize host (lowercase, strip trailing dot)
    hostname = parsed.hostname.lower().rstrip(".")
    if not hostname:
        raise ValueError(f"Missing hostname in URL: {service_url!r}")

    # Domain must be in the approved list
    if hostname not in APPROVED_DOMAINS:
        raise ValueError(f"Domain {hostname!r} is not approved")

    # Resolve the hostname to IP addresses
    try:
        addrinfo = socket.getaddrinfo(hostname, None, family=socket.AF_INET)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname {hostname!r}: {exc}") from exc

    # Ensure at least one IP is public
    for entry in addrinfo:
        ip = entry[4][0]
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP {ip!r} for {hostname!r} is private/internal")

    # Reconstruct a clean URL (strip fragments, keep query)
    cleaned = parsed._replace(fragment="").geturl()

    return cleaned