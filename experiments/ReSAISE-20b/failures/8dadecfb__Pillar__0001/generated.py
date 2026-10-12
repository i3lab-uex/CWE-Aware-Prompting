import re
from urllib.parse import urlparse, urlunparse

# List of domains that are considered safe for redirection
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "safe-redirect.net",
}

# Regex to match a valid hostname (IPv4, IPv6 or domain)
HOSTNAME_RE = re.compile(
    r"^(?:"
    # IPv4
    r"(?:\d{1,3}\.){3}\d{1,3}"
    r"|"
    # IPv6
    r"\[?[0-9a-fA-F:]+\]?"
    r"|"
    # Domain name
    r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
    r")$",
    re.IGNORECASE,
)

def _is_approved(host: str) -> bool:
    """
    Return True if the host is in the approved list or a sub‑domain of an approved domain.
    """
    host = host.lower()
    if not HOSTNAME_RE.match(host):
        return False
    # Strip IPv6 brackets for matching
    if host.startswith("[") and host.endswith("]"):
        host = host[1:-1]
    # Exact match
    if host in APPROVED_DOMAINS:
        return True
    # Sub‑domain check
    for approved in APPROVED_DOMAINS:
        if host.endswith("." + approved):
            return True
    return False

def validate_redirect_url(input_url: str) -> str:
    """
    Validate a user supplied URL and return it only if its domain is approved.
    
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
        If the URL is malformed, uses an unsafe scheme, or its domain is not approved.
    """
    # Parse the URL
    parsed = urlparse(input_url)

    # Scheme must be http or https
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # netloc must be present
    if not parsed.netloc:
        raise ValueError("URL does not contain a network location")

    # Validate host
    if not _is_approved(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not approved for redirection")

    # Reconstruct the URL to ensure no hidden characters
    safe_url = urlunparse(parsed)
    return safe_url