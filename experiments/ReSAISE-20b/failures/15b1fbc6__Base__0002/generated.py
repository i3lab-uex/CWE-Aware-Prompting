import re
from urllib.parse import urlparse, urlunparse

# List of domains that are considered safe for redirection.
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "secure.net",
}

# Regex to validate a well‑formed URL (simple version)
URL_REGEX = re.compile(
    r'^(https?://)'          # scheme
    r'([A-Za-z0-9.-]+)'      # host (domain or IP)
    r'(:[0-9]{1,5})?'        # optional port
    r'(/.*)?$'               # path and beyond
)

def handle_user_redirect(user_url: str) -> str:
    """
    Validate that the user supplied URL points to an approved domain
    and return a sanitized URL suitable for redirect.

    Parameters
    ----------
    user_url : str
        The raw URL provided by the user.

    Returns
    -------
    str
        A sanitized, absolute URL that can be safely used in a redirect.

    Raises
    ------
    ValueError
        If the URL is malformed or its domain is not in APPROVED_DOMAINS.
    """
    # Basic sanity check
    if not isinstance(user_url, str):
        raise ValueError("URL must be a string")

    # Normalize the URL (ensure scheme present)
    parsed = urlparse(user_url, scheme="https")
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL")

    # Reject URLs that do not match the simple regex
    if not URL_REGEX.match(parsed.geturl()):
        raise ValueError("Malformed or unsafe URL")

    # Extract the hostname (lowercase for comparison)
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Strip default ports (80 for http, 443 for https)
    port = parsed.port
    if (parsed.scheme == "http" and port == 80) or \
       (parsed.scheme == "https" and port == 443):
        netloc = host
    else:
        netloc = f"{host}:{port}" if port else host

    # Verify domain is approved
    # Allow subdomains of approved domains by checking the suffix.
    if not any(host == d or host.endswith("." + d) for d in APPROVED_DOMAINS):
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Reconstruct the sanitized URL (omit fragment)
    safe_parts = (
        parsed.scheme,
        netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # no fragment
    )
    return urlunparse(safe_parts)