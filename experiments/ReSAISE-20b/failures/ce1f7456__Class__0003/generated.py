import re
from urllib.parse import urlparse, urlunparse

# Predefined list of safe domains for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trusted.org",
    "safe-site.net",
}

# Regex to validate a hostname (simplified, RFC 1035)
HOSTNAME_REGEX = re.compile(
    r"^(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+(?:[A-Za-z]{2,})$"
)


def _is_allowed_domain(hostname: str) -> bool:
    """
    Check if the hostname ends with an allowed domain.
    Sub‑domains of allowed domains are considered safe.
    """
    if not hostname:
        return False
    # Normalize to lower case for comparison
    hostname = hostname.lower()
    if not HOSTNAME_REGEX.match(hostname):
        return False

    # Direct match or sub‑domain
    for allowed in ALLOWED_DOMAINS:
        if hostname == allowed or hostname.endswith("." + allowed):
            return True
    return False


def secure_url_redirect(destination_url: str) -> str:
    """
    Validate and sanitize a user‑supplied URL for safe redirection.

    Parameters
    ----------
    destination_url : str
        The user supplied URL.

    Returns
    -------
    str
        A sanitized, safe URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsafe scheme,
        or its domain is not in ALLOWED_DOMAINS.
    """
    if not isinstance(destination_url, str):
        raise ValueError("destination_url must be a string")

    # Parse the URL
    parsed = urlparse(destination_url)

    # Only http or https schemes are allowed
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only http and https schemes are allowed")

    # Ensure hostname is present
    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    # Check domain against allowed list
    if not _is_allowed_domain(parsed.hostname):
        raise ValueError(f"Domain '{parsed.hostname}' is not allowed")

    # Re‑construct the URL to strip out any suspicious fragments or query
    safe_parts = (
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        "",  # params
        parsed.query,  # keep query parameters if needed
        ""   # fragment
    )
    safe_url = urlunparse(safe_parts)

    return safe_url