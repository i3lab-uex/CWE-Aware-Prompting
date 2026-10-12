import re
from urllib.parse import urlparse, urlunparse

# List of domains that are considered safe for redirection.
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "safe-site.net"
}

# Regular expression to validate that the URL scheme is HTTP or HTTPS.
_SCHEME_RE = re.compile(r"^(https?)://", re.IGNORECASE)


def secure_user_redirect(url_input: str) -> str:
    """
    Validate and sanitize a user-provided URL before redirecting.

    Parameters
    ----------
    url_input : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A fully qualified, safe-to-use URL that can be sent to the client for redirection.

    Raises
    ------
    ValueError
        If the URL does not contain an approved domain, or if it uses an unsafe scheme.
    """
    # Parse the URL
    parsed = urlparse(url_input)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL: missing scheme or host")

    # Only allow http/https schemes
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP/HTTPS are allowed.")

    # Normalize the host to lowercase and strip leading/trailing whitespace
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Basic check for IP addresses (block all numeric hosts)
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host):
        raise ValueError("Direct IP addresses are not allowed")

    # Verify the domain is in the approved list
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Reconstruct the URL to ensure it has a standard form
    safe_parsed = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=f"{host}:{parsed.port}" if parsed.port else host,
    )
    safe_url = urlunparse(safe_parsed)

    # Ensure the resulting URL still starts with http:// or https://
    if not _SCHEME_RE.match(safe_url):
        raise ValueError("Sanitization failed: URL does not start with http:// or https://")

    return safe_url