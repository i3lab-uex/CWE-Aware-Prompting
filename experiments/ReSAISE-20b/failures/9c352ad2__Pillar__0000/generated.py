import re
from urllib.parse import urlparse

# --------------------------------------------------------------------------- #
# 1. Pre‑approved public API domains
# --------------------------------------------------------------------------- #
PRE_APPROVED_DOMAINS = {
    "api.example.com",
    "data.provider.net",
    "service.mycompany.org",
}

# --------------------------------------------------------------------------- #
# 2. Regular expressions for internal IP ranges (RFC1918)
# --------------------------------------------------------------------------- #
INTERNAL_IP_PATTERNS = [
    re.compile(r"^10\."),               # 10.0.0.0/8
    re.compile(r"^172\.(1[6-9]|2\d|3[0-1])\."),
    re.compile(r"^192\.168\."),
]

# --------------------------------------------------------------------------- #
# 3. Helper functions
# --------------------------------------------------------------------------- #
def _is_internal_ip(host: str) -> bool:
    """
    Detect if a host string represents an internal IP address.
    Handles IPv4 dotted decimal notation only; IPv6 and hostname
    resolution are considered safe because we only allow known domains.
    """
    for pattern in INTERNAL_IP_PATTERNS:
        if pattern.match(host):
            return True
    return False


def _normalize_domain(host: str) -> str:
    """
    Normalise the host part by removing trailing dots and converting
    to lower case. This avoids subtle mismatches such as 'API.EXAMPLE.COM.'
    """
    return host.rstrip(".").lower()


# --------------------------------------------------------------------------- #
# 4. Main function
# --------------------------------------------------------------------------- #
def process_webhook(webhook_url: str) -> str:
    """
    Validate that a webhook URL points to a pre‑approved public API endpoint.

    Parameters
    ----------
    webhook_url : str
        The URL provided by an external service.

    Returns
    -------
    str
        The validated, normalised URL that points to an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an unapproved domain,
        or attempts to access internal resources.
    """
    if not webhook_url:
        raise ValueError("Webhook URL must be a non‑empty string")

    parsed = urlparse(webhook_url)

    # Basic URL sanity checks
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http/https allowed.")
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain or IP)")

    # Split host and optional port
    host = parsed.hostname  # hostname is lower‑case by urlparse
    if host is None:
        raise ValueError("Could not parse hostname from URL")

    # Reject internal IP addresses
    if _is_internal_ip(host):
        raise ValueError("URL points to an internal IP address")

    # Normalise the host for comparison
    normalized_host = _normalize_domain(host)

    # Ensure the domain is in our whitelist
    if normalized_host not in PRE_APPROVED_DOMAINS:
        raise ValueError(f"Domain '{normalized_host}' is not in the approved list")

    # Re‑build a clean URL to avoid accidental path manipulation
    safe_url = parsed._replace(netloc=f"{normalized_host}{':' + str(parsed.port) if parsed.port else ''}")
    return safe_url.geturl()