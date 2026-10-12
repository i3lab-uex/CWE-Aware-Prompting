import re
from urllib.parse import urlparse, urlunparse

# List of approved external domains (case‑insensitive)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "secure.net",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

def _normalize_domain(domain: str) -> str:
    """
    Normalise a domain for comparison:
      * lower‑case
      * strip leading/trailing whitespace
    """
    return domain.strip().lower()

def process_url_redirect(input_url: str) -> str:
    """
    Validate and return a safe URL for redirection.

    Parameters
    ----------
    input_url : str
        The user supplied URL to be redirected to.

    Returns
    -------
    str
        A validated, safe‑to‑use URL.

    Raises
    ------
    ValueError
        If the domain is not in the approved list or the scheme is disallowed.
    """
    if not isinstance(input_url, str):
        raise TypeError("input_url must be a string")

    # Parse the URL
    parsed = urlparse(input_url)

    # Ensure scheme is present and allowed
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported scheme: {parsed.scheme!r}")

    # Extract hostname (netloc may include port)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Normalise domain for comparison
    host_norm = _normalize_domain(host)

    # Check against approved domains (exact match or subdomain of an approved domain)
    if not any(
        host_norm == ad or host_norm.endswith("." + ad) for ad in APPROVED_DOMAINS
    ):
        raise ValueError(f"Domain {host!r} is not approved for redirection")

    # Re‑construct the URL to ensure no malicious fragments or query tricks
    safe_parts = (
        parsed.scheme,
        parsed.netloc,          # includes hostname and optional port
        parsed.path,
        parsed.params,
        parsed.query,
        ""  # discard fragment
    )
    safe_url = urlunparse(safe_parts)

    return safe_url