import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (example)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "api.safe-domain.net",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"^(127\.|10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.)"
)

def _is_private_ip(host: str) -> bool:
    """Check if the host is a private IP address."""
    try:
        # Simple check using regex; full validation can use ipaddress module
        return bool(PRIVATE_IP_REGEX.match(host))
    except Exception:
        return False

def process_url_redirect(input_url: str) -> str:
    """
    Validate and sanitize a user-provided URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The URL supplied by the user.

    Returns
    -------
    str
        A validated, safe-to-use URL for redirection.

    Raises
    ------
    ValueError
        If the URL's domain is not in the approved list, or if it points to a private IP,
        uses an unsupported scheme, or is otherwise malformed.
    """
    if not input_url:
        raise ValueError("Empty URL provided")

    # Parse the URL
    parsed = urlparse(input_url)

    # Only allow http or https schemes
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Extract host (domain or IP)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject private IP addresses to mitigate SSRF
    if _is_private_ip(host):
        raise ValueError("URL points to a private IP address")

    # Normalize host for comparison (case-insensitive)
    host_lower = host.lower()

    # Check against approved domains
    if host_lower not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Reconstruct the URL to ensure it's canonical
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        parsed.query or "",
        ""   # fragment
    ))

    return safe_url