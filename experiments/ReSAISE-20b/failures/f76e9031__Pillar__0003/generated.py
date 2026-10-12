import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (add or remove as needed)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "safe-portal.net",
}

# Regular expression to validate a hostname (RFC 1035 compliant)
HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}$"
)

def _is_valid_hostname(hostname: str) -> bool:
    """Return True if the hostname is syntactically valid."""
    return bool(HOSTNAME_RE.match(hostname))

def _normalize_hostname(hostname: str) -> str:
    """
    Normalise hostname for comparison.
    - Convert to lowercase
    - Decode punycode (IDNA)
    """
    try:
        # IDNA encoding/decoding handles Unicode domain names
        return hostname.encode("idna").decode("ascii").lower()
    except Exception:
        # If encoding fails, treat as invalid
        return ""

def redirect_user_safely(target_url: str) -> str:
    """
    Validate and return a safe URL for redirection.

    Parameters
    ----------
    target_url : str
        User supplied URL to redirect to.

    Returns
    -------
    str
        Normalised, validated URL safe for redirection.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP/HTTPS, or its domain is not approved.
    """
    if not isinstance(target_url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(target_url)

    # Only http and https are allowed
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Extract hostname; ensure it is present
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Validate hostname syntax
    if not _is_valid_hostname(hostname):
        raise ValueError(f"Invalid hostname: {hostname}")

    # Normalise for comparison
    norm_hostname = _normalize_hostname(hostname)

    if not norm_hostname:
        raise ValueError("Hostname normalization failed")

    # Check against approved domains (exact match)
    if norm_hostname not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{norm_hostname}' is not approved")

    # Reconstruct the URL to ensure no fragments or query parameters
    safe_url = urlunparse((
        parsed.scheme.lower(),
        norm_hostname,
        parsed.path or "",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return safe_url

# Example usage (uncomment to test):
# try:
#     print(redirect_user_safely("https://example.com/welcome"))
# except ValueError as e:
#     print(f"Redirection blocked: {e}")