import re
from urllib.parse import urlparse, urlunparse

# List of approved domains. Subdomains are allowed if the base domain matches.
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.io"
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def _is_approved_domain(netloc: str) -> bool:
    """
    Check if the given netloc ends with an approved domain.
    The check is case‑insensitive and ignores ports.
    """
    # Strip port if present
    host = netloc.split(":")[0].lower()
    return any(host == domain or host.endswith("." + domain) for domain in APPROVED_DOMAINS)


def validate_redirect_url(input_url: str) -> str:
    """
    Validate a user‑supplied URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A sanitized, validated URL that can be safely used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses a disallowed scheme,
        or its domain is not in the approved list.
    """
    # Basic parsing
    parsed = urlparse(input_url)

    if not parsed.scheme or parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Disallowed or missing scheme: {parsed.scheme}")

    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    if not _is_approved_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not approved")

    # Re‑assemble the URL to ensure it hasn't been tampered with
    sanitized = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))

    # Quick sanity check: ensure the sanitized URL still contains the same domain
    if not _is_approved_domain(urlparse(sanitized).netloc):
        raise ValueError("Sanitization failed: domain changed")

    return sanitized