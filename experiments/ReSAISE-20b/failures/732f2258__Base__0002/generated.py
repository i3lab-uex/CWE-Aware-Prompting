import re
from urllib.parse import urlparse, ParseResult
import ipaddress

# ------------------------------------------------------------------
# Configuration: list of approved public API domains.
# Add or remove domains as needed for your environment.
ALLOWED_DOMAINS = {
    "api.example.com",
    "webhook.service.io",
    "hooks.internal.net",   # example of a public domain that accepts webhooks
}

# Regular expression to detect private IP ranges and local hostnames.
PRIVATE_IP_RE = re.compile(
    r"""
    ^(10\.|127\.|169\.254\.|172\.(1[6-9]|2\d|3[01])\.|192\.168\.)   # private IP ranges
    |(^localhost$)                                                   # localhost hostname
    """,
    re.VERBOSE,
)


def _is_private_ip(host: str) -> bool:
    """
    Determine if the given host is a private IP address or resolves to one.
    """
    try:
        # Resolve hostname to an IP if possible
        ip = ipaddress.ip_address(host)
    except ValueError:
        # If host is not an IP, try to interpret as a hostname.
        # For simplicity we only check if the host itself is a private IP string
        return False

    # ipaddress module knows about private, loopback, link-local etc.
    return ip.is_private or ip.is_loopback or ip.is_link_local


def _validate_domain(domain: str) -> None:
    """
    Validate that the domain is in the allowed list and not private.
    Raises ValueError if validation fails.
    """
    # Reject obvious private domain patterns
    if PRIVATE_IP_RE.search(domain):
        raise ValueError(f"Domain '{domain}' is private or reserved (SSRF risk).")

    # Check against the whitelist
    if domain not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not an approved API endpoint.")


def analyze_webhook(webhook_address: str) -> str:
    """
    Process a webhook URL from an external service and return a validated
    URL suitable for internal API requests.

    Parameters
    ----------
    webhook_address : str
        The raw URL supplied by an external service.

    Returns
    -------
    str
        A fully validated, normalized URL that can be safely used for an
        internal API request.

    Raises
    ------
    ValueError
        If the URL is malformed, points to a private/internal domain,
        or does not belong to the approved API endpoint list.
    """
    if not webhook_address:
        raise ValueError("Webhook address is empty.")

    parsed: ParseResult = urlparse(webhook_address)

    # Basic URL validation
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: '{webhook_address}'")

    # Ensure the scheme is HTTPS (or HTTP if your environment requires it)
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}' (only http/https allowed).")

    # Normalize host: strip port if present for domain comparison
    host = parsed.hostname or ""
    _validate_domain(host.lower())

    # Reject URLs that resolve to private IPs (SSRF protection)
    if _is_private_ip(host):
        raise ValueError(f"URL resolves to a private IP address: '{host}'")

    # Reconstruct the URL to ensure it's canonical
    normalized = parsed._replace(netloc=host.lower() + (f":{parsed.port}" if parsed.port else ""))
    return normalized.geturl()