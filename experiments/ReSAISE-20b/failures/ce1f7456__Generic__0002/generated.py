import re
from urllib.parse import urlparse, urlunparse, ParseResult

# Define the set of allowed domains (case‑insensitive)
ALLOWED_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "myapp.local",
}

# Regular expression to validate domain format (basic RFC‑1035)
_DOMAIN_RE = re.compile(r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$")


def _is_allowed_domain(host: str) -> bool:
    """
    Check if the host matches one of the allowed domains.
    Subdomains are permitted only when explicitly listed in ALLOWED_DOMAINS.
    """
    host = host.lower()
    if host in ALLOWED_DOMAINS:
        return True

    # Optional: allow subdomains of a base domain if the base is allowed
    for domain in ALLOWED_DOMAINS:
        if host.endswith("." + domain):
            return True
    return False


def secure_url_redirect(destination_url: str) -> str:
    """
    Validate and sanitize a user‑supplied URL for redirection.

    Parameters
    ----------
    destination_url : str
        The URL provided by the user for redirection.

    Returns
    -------
    str
        A sanitized URL that is safe to redirect to.

    Raises
    ------
    ValueError
        If the URL's domain is not in ALLOWED_DOMAINS or if the URL is malformed.
    """
    # Parse the input URL
    parsed = urlparse(destination_url)

    # Reject URLs without a scheme or netloc (e.g., relative paths)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute with a scheme and domain")

    # Ensure the scheme is HTTP or HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only http and https schemes are allowed")

    # Validate the domain
    if not _DOMAIN_RE.match(parsed.netloc):
        raise ValueError("Invalid domain format")

    if not _is_allowed_domain(parsed.hostname or ""):
        raise ValueError(f"Domain '{parsed.hostname}' is not allowed")

    # Remove fragment to avoid unwanted navigation
    sanitized = ParseResult(
        scheme=parsed.scheme,
        netloc=parsed.netloc,
        path=parsed.path or "/",
        params=parsed.params,
        query=parsed.query,
        fragment="",
    )
    return urlunparse(sanitized)