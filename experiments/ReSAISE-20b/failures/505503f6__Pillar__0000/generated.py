import re
from urllib.parse import urlparse, urlunparse

# Pre‑approved external domains (exact matches or subdomains)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "safe-domain.net",
}

# Regex to detect subdomains of approved domains
DOMAIN_REGEX = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*"
    r"(?P<base_domain>(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?))$"
)


def _is_approved_domain(domain: str) -> bool:
    """
    Check whether the supplied domain is an exact match or a subdomain of one
    of the approved domains.
    """
    if domain in APPROVED_DOMAINS:
        return True

    # Check for subdomains
    match = DOMAIN_REGEX.match(domain)
    if not match:
        return False

    base_domain = match.group("base_domain")
    # Walk up the domain hierarchy
    parts = domain.split(".")
    for i in range(len(parts) - 1):
        candidate = ".".join(parts[i:])
        if candidate in APPROVED_DOMAINS:
            return True
    return False


def validate_safe_redirect(input_link: str) -> str:
    """
    Validate that a user supplied URL points to an approved domain.
    
    Parameters
    ----------
    input_link : str
        The URL supplied by the user.

    Returns
    -------
    str
        The same URL if it is safe for redirection.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https, or the domain is not approved.
    """
    # Basic sanity check: must be a string
    if not isinstance(input_link, str):
        raise ValueError("input_link must be a string")

    parsed = urlparse(input_link)

    # Reject relative URLs or missing scheme
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute with scheme and netloc")

    # Only http/https schemes are allowed
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only http and https schemes are allowed")

    # Normalize domain to lower case
    domain = parsed.hostname.lower() if parsed.hostname else ""
    if not _is_approved_domain(domain):
        raise ValueError(f"Domain '{domain}' is not approved for redirection")

    # Re‑build the URL to ensure no unwanted components
    safe_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            "",  # drop fragment for safety
        )
    )

    return safe_url