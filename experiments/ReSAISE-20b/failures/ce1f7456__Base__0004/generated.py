import re
from urllib.parse import urlparse, urlunparse

# Predefined list of safe domains (including subdomains)
ALLOWED_DOMAINS = {
    "example.com",
    "trusted.org",
    "safe-site.net",
}

# Regular expression to detect IP addresses (both IPv4 and IPv6)
_IP_REGEX = re.compile(
    r"""
    ^(?:
        # IPv4
        (?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})
        |
        # IPv6
        \[?(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}\]?
    )$
    """,
    re.VERBOSE,
)


def _is_ip_address(host: str) -> bool:
    """Return True if the host is an IP address."""
    return bool(_IP_REGEX.match(host))


def _normalize_domain(domain: str) -> str:
    """Normalize domain by lower‑casing and stripping trailing dot."""
    return domain.lower().rstrip(".")


def _is_allowed_domain(host: str) -> bool:
    """Check if the host is in ALLOWED_DOMAINS or a sub‑domain of one."""
    host = _normalize_domain(host)

    # Disallow IP addresses unless explicitly whitelisted
    if _is_ip_address(host):
        return False

    for allowed in ALLOWED_DOMAINS:
        allowed = _normalize_domain(allowed)
        if host == allowed or host.endswith("." + allowed):
            return True
    return False


def secure_url_redirect(destination_url: str) -> str:
    """
    Validate a user‑supplied URL and return a sanitized version
    suitable for redirection.

    Parameters
    ----------
    destination_url : str
        The URL provided by the user for redirection.

    Returns
    -------
    str
        A sanitized absolute URL that is safe to redirect to.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https or its domain is not in
        ALLOWED_DOMAINS.
    """
    if not destination_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(destination_url)

    # Enforce http/https scheme
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Ensure a hostname is present
    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    # Check domain against whitelist
    if not _is_allowed_domain(parsed.hostname):
        raise ValueError(f"Domain '{parsed.hostname}' is not allowed")

    # Re‑build the URL to strip any unsafe fragments or parameters
    safe_parts = (
        parsed.scheme,
        parsed.netloc,  # includes hostname and optional port
        parsed.path or "/",
        "",            # params (rarely used)
        parsed.query,  # allow query parameters
        "",            # fragment (strip it)
    )
    sanitized_url = urlunparse(safe_parts)

    return sanitized_url