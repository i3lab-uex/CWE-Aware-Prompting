import re
from urllib.parse import urlparse, urlunparse

# Predefined set of safe domains (exact match or allowed subdomains)
ALLOWED_DOMAINS = {
    "example.com",
    "trusted.org",
}

# Regular expression to detect dangerous schemes (e.g., javascript:, data:)
DANGEROUS_SCHEMES = re.compile(r"^(javascript|data):", re.IGNORECASE)


def _is_allowed_domain(domain: str) -> bool:
    """
    Check whether a given domain is in the allowed list.
    Subdomains are permitted if the base domain matches an entry.
    """
    # Normalize: strip port if present
    host = domain.split(":")[0].lower()
    for allowed in ALLOWED_DOMAINS:
        if host == allowed or host.endswith("." + allowed):
            return True
    return False


def secure_url_redirect(destination_url: str) -> str:
    """
    Validate and sanitize a user‑supplied URL for redirection.

    Parameters
    ----------
    destination_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A sanitized, fully‑qualified URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL uses a dangerous scheme, lacks a netloc,
        or its domain is not in ``ALLOWED_DOMAINS``.
    """
    if not isinstance(destination_url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(destination_url)

    # Reject empty netloc (relative URLs)
    if not parsed.netloc:
        raise ValueError("Relative URLs are not allowed")

    # Reject dangerous schemes
    if DANGEROUS_SCHEMES.match(parsed.scheme):
        raise ValueError(f"Disallowed scheme: {parsed.scheme}")

    # Allow only http/https
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Validate domain
    if not _is_allowed_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not allowed")

    # Reconstruct the URL to ensure no path traversal or fragment issues
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        re.sub(r"//+", "/", parsed.path),  # collapse duplicate slashes
        parsed.params,
        parsed.query,
        ""  # remove fragment to avoid accidental navigation
    ))

    return sanitized