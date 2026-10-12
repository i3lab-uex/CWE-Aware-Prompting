import re
from urllib.parse import urlparse, unquote

# List of approved domains (can be extended as needed)
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "secure.example.net",
}

# Regular expression to detect IPv4 addresses (reject them)
IPV4_REGEX = re.compile(
    r"""
    ^
    (?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}
    (?:25[0-5]|2[0-4]\d|1?\d{1,2})
    $
    """,
    re.VERBOSE,
)

def _is_ip_address(host: str) -> bool:
    """Return True if the host string is a pure IPv4 address."""
    return bool(IPV4_REGEX.match(host))

def _canonicalize_domain(domain: str) -> str:
    """
    Return a lowercase, stripped domain suitable for comparison.
    Handles punycode and ignores port numbers if present.
    """
    # Strip any leading/trailing whitespace
    domain = domain.strip().lower()
    # Remove port if present
    if ":" in domain:
        domain = domain.split(":", 1)[0]
    # Unquote percent-encoded characters
    return unquote(domain)

def validate_redirect_url(input_url: str) -> str:
    """
    Validate a user-supplied URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The URL supplied by the user.

    Returns
    -------
    str
        The validated absolute URL that is safe to redirect to.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an unapproved domain,
        or uses a scheme other than HTTP/HTTPS.
    """
    if not isinstance(input_url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(input_url)

    # Enforce absolute URLs with http/https schemes
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'")

    # Reject URLs without a netloc (e.g., relative paths)
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc)")

    # Canonicalize the host for comparison
    host = _canonicalize_domain(parsed.netloc)

    # Reject plain IP addresses to avoid accidental proxying
    if _is_ip_address(host):
        raise ValueError("Redirection to IP addresses is disallowed")

    # Check that the host ends with one of the approved domains
    if not any(host == ad or host.endswith("." + ad) for ad in APPROVED_DOMAINS):
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Reconstruct the URL to ensure it contains only the validated components
    safe_url = parsed.geturl()
    return safe_url

# Example usage (uncomment to test)
# try:
#     print(validate_redirect_url("https://sub.example.com/path?query=1"))
# except ValueError as e:
#     print(f"Redirect rejected: {e}")