import re
from urllib.parse import urlparse

# List of domains that are considered safe for redirection.
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    # Add other domains here.
}

# Regular expression to validate a hostname (RFC 1035 compliant).
HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+"
    r"[a-zA-Z]{2,}$"
)


def _is_valid_hostname(hostname: str) -> bool:
    """
    Return True if the hostname matches a standard DNS hostname pattern.
    This also rejects IP addresses, which are not considered safe in this context.
    """
    return bool(HOSTNAME_RE.match(hostname))


def _extract_domain(netloc: str) -> str:
    """
    Extract the hostname from a netloc, ignoring any port.
    If the netloc is an IP address or malformed, raise ValueError.
    """
    # Strip userinfo if present
    if "@" in netloc:
        _, host_port = netloc.rsplit("@", 1)
    else:
        host_port = netloc

    # Separate hostname and port
    if ":" in host_port:
        host, _ = host_port.split(":", 1)
    else:
        host = host_port

    # Reject IP addresses (both IPv4 and IPv6)
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host):
        raise ValueError("IP addresses are not allowed for redirection")

    if re.match(r"^\[.*\]$", host):  # IPv6 literal
        raise ValueError("IPv6 addresses are not allowed for redirection")

    host = host.lower()
    if not _is_valid_hostname(host):
        raise ValueError(f"Invalid hostname: {host}")

    return host


def validate_redirect_url(input_url: str) -> str:
    """
    Validate that the user supplied URL is safe for redirection.

    Parameters
    ----------
    input_url : str
        The URL supplied by the user.

    Returns
    -------
    str
        The original URL if it is safe for redirection.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https, or if its domain is not in the approved list.
    """
    parsed = urlparse(input_url)

    # Ensure we have an absolute URL with http/https scheme
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP/HTTPS URLs are allowed")

    # Ensure the netloc is present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc)")

    domain = _extract_domain(parsed.netloc)

    # Check if the domain is approved
    if domain not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved for redirection")

    # All checks passed – return the original URL
    return input_url