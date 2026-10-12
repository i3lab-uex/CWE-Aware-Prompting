import re
from urllib.parse import urlparse, urlunparse

# Whitelist of approved external domains (case‑insensitive)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "cdn.safe-domain.net",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def validate_safe_redirect(input_link: str) -> str:
    """
    Validate a user supplied URL and ensure it points to an approved domain.
    
    Parameters
    ----------
    input_link : str
        The URL supplied by the user.

    Returns
    -------
    str
        A fully-qualified, safe-to-use URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses a disallowed scheme, or points to an unapproved domain.
    """
    if not isinstance(input_link, str):
        raise ValueError("URL must be a string")

    # Strip leading/trailing whitespace
    input_link = input_link.strip()

    # Reject URLs that are empty or just a fragment/hash
    if not input_link or input_link.startswith("#"):
        raise ValueError("URL is empty or only a fragment")

    # Parse the URL
    parsed = urlparse(input_link)

    # Handle relative URLs: treat them as unsafe in this context
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Relative URLs are not allowed")

    # Enforce allowed schemes
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Disallowed URL scheme: {parsed.scheme}")

    # Normalise the domain to lowercase and strip port if present
    hostname = parsed.hostname.lower() if parsed.hostname else ""
    # If a port is present, ignore it for domain checking
    domain = hostname.split(":")[0]

    # Reject IP addresses (both IPv4 and IPv6) unless they are explicitly whitelisted
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain) or re.match(r"^\[.*\]$", domain):
        # IP addresses are not allowed unless explicitly whitelisted
        if domain not in APPROVED_DOMAINS:
            raise ValueError("IP addresses are not allowed")

    # Verify the domain is in the whitelist
    if domain not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved for redirection")

    # Rebuild the URL to ensure canonical form
    safe_url = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))

    return safe_url