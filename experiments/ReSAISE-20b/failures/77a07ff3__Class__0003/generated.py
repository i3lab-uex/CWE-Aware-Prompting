import re
from urllib.parse import urlparse, urlunparse

# A list of pre‑approved domains (case‑insensitive).  Add your own entries here.
APPROVED_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "mycompany.co.uk",
}

# Regular expression to detect IP addresses (IPv4 or IPv6) in the hostname.
_IP_REGEX = re.compile(
    r"^(?:\d{1,3}\.){3}\d{1,3}$|^\[?[0-9a-fA-F:]+\]?$"
)

def _is_ip_address(hostname: str) -> bool:
    """Return True if the hostname looks like an IP address."""
    return bool(_IP_REGEX.match(hostname))

def process_url_redirect(input_url: str) -> str:
    """
    Validate a user‑supplied URL and return it only if its domain is approved.

    Parameters
    ----------
    input_url : str
        The URL supplied by the user that may be used for redirection.

    Returns
    -------
    str
        The validated URL, suitable for safe redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, contains an IP address, or its domain is not approved.
    """
    if not isinstance(input_url, str):
        raise ValueError("URL must be a string")

    # Parse the URL; reject if scheme is missing or not http/https.
    parsed = urlparse(input_url)
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only http and https schemes are allowed")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Reject IP addresses to avoid confusion with the product acting as a proxy.
    if _is_ip_address(hostname):
        raise ValueError("IP addresses are not allowed as redirect targets")

    # Normalize the hostname to lower‑case for comparison.
    domain = hostname.lower()

    if domain not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved for redirection")

    # Re‑assemble the URL to ensure no additional fragments or queries that
    # could alter behaviour (you may decide to preserve them instead).
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        parsed.query,  # preserve query if needed
        ""   # fragment removed for safety
    ))

    return safe_url