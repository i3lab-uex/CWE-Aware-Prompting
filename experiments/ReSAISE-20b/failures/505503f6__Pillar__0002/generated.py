import re
from urllib.parse import urlparse, urlunparse

# List of pre‑approved domains (example entries)
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "myapp.io",
}

# Regular expression for a safe domain (allows subdomains)
SAFE_DOMAIN_RE = re.compile(r"^(?:[a-z0-9](?:[a-z0-9\-]{0,61}[a-z0-9])?\.)+[a-z]{2,}$", re.IGNORECASE)


def validate_safe_redirect(input_link: str) -> str:
    """
    Validate a user‑supplied URL for safe redirection.

    Parameters
    ----------
    input_link : str
        The URL provided by the user.

    Returns
    -------
    str
        A validated, fully qualified URL that can be safely used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsafe scheme, or its domain is not approved.
    """
    # Parse the URL
    parsed = urlparse(input_link)

    # Reject relative URLs, fragments or paths that might cause confusion
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute with scheme and domain")

    # Only allow http or https schemes
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only http and https schemes are allowed")

    # Normalize domain (lowercase, strip trailing dots)
    host = parsed.hostname.lower().rstrip(".")
    if not host or not SAFE_DOMAIN_RE.match(host):
        raise ValueError("Invalid domain format")

    # Ensure the host is in the approved list (including subdomains)
    if not any(host == domain or host.endswith("." + domain) for domain in APPROVED_DOMAINS):
        raise ValueError(f"Domain '{host}' is not approved for redirects")

    # Re‑assemble the URL to ensure no unintended components remain
    safe_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "/",
            "",  # params
            parsed.query,
            "",  # fragment removed
        )
    )

    return safe_url