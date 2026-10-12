import re
from urllib.parse import urlparse, urlunparse

# Predefined safe domains (exact matches or subdomains)
SAFE_DOMAINS = {
    "example.com",
    "trusted.org",
    "secure.net",
}

# Regular expression to validate that a domain is within the allowed set
DOMAIN_PATTERN = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a‑zA‑Z0‑9\-]{0,61}[a‑zA‑Z0‑9])?\.)+"  # subdomains
    r"(?P<root>(?:[a-zA-Z]{2,}))$"
)

def _is_allowed_domain(domain: str) -> bool:
    """
    Check whether the given domain or any of its parent domains are in SAFE_DOMAINS.
    """
    # Normalize to lower case
    domain = domain.lower()
    parts = domain.split('.')
    for i in range(len(parts)):
        candidate = '.'.join(parts[i:])
        if candidate in SAFE_DOMAINS:
            return True
    return False

def secure_url_redirect(destination_url: str) -> str:
    """
    Sanitize a user‑supplied URL for safe redirection.

    Parameters
    ----------
    destination_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A fully qualified, sanitized URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsafe scheme, or its domain is not in SAFE_DOMAINS.
    """
    if not isinstance(destination_url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(destination_url)

    # Only allow http and https schemes
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Ensure a host is present
    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    # Extract the domain (ignore userinfo, port)
    host = parsed.hostname
    if not host:
        raise ValueError("Unable to parse hostname")

    # Validate domain against SAFE_DOMAINS
    if not _is_allowed_domain(host):
        raise ValueError(f"Domain '{host}' is not allowed")

    # Reconstruct a clean URL (strip fragments, query can be preserved if needed)
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",          # params
        parsed.query,  # preserve query if present
        ""           # strip fragment to avoid redirects to anchors
    ))

    return sanitized