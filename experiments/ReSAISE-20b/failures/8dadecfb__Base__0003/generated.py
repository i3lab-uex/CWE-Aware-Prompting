import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (example)
APPROVED_DOMAINS = {
    "example.com",
    "trusted.example.org",
    "myapp.local",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

def validate_redirect_url(input_url: str) -> str:
    """
    Validate a user-supplied URL and return it only if its domain is approved.
    
    Parameters
    ----------
    input_url : str
        The URL provided by the user.

    Returns
    -------
    str
        The sanitized, validated absolute URL that can be safely redirected to.

    Raises
    ------
    ValueError
        If the URL is malformed, uses a disallowed scheme, or its domain is not in
        the approved list.
    """
    # Parse the URL
    parsed = urlparse(input_url)

    # Reject relative URLs or missing scheme
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute with scheme and netloc")

    # Scheme check
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Normalize host (case-insensitive)
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Optional: strip port for domain comparison
    host_without_port = host.split(":")[0]

    # Check against approved domains
    if host_without_port not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host_without_port}' is not approved")

    # Reconstruct the URL to ensure canonical form
    safe_url = urlunparse((
        parsed.scheme,
        host_without_port + (f":{parsed.port}" if parsed.port else ""),
        parsed.path,
        parsed.params,
        parsed.query,
        parsed.fragment
    ))
    return safe_url