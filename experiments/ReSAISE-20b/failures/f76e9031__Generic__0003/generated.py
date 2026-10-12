import re
from urllib.parse import urlparse, urlunparse

# A list of approved domains. Add any domain you consider safe for redirection.
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "mydomain.net",
}

# Regular expression to detect potentially malicious schemes or characters.
SAFE_URL_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://")

def redirect_user_safely(target_url: str) -> str:
    """
    Validate that a user‑supplied URL is safe for redirection.

    Parameters
    ----------
    target_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A fully‑qualified, validated URL safe for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsafe scheme, or its domain
        is not in the approved list.
    """
    # Basic sanity check: URL must contain a scheme.
    if not SAFE_URL_RE.match(target_url):
        raise ValueError("URL must begin with a valid scheme (e.g., http:// or https://).")

    parsed = urlparse(target_url)

    # Reject unsupported schemes.
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Reject URLs with empty netloc (e.g., relative paths or missing host).
    if not parsed.netloc:
        raise ValueError("URL must contain a valid domain.")

    # Normalize the hostname (case‑insensitive) and strip any port.
    host = parsed.hostname.lower()
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for redirection.")

    # Reconstruct the URL to ensure it contains only the allowed components.
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        parsed.query,
        ""   # fragment
    ))

    return safe_url