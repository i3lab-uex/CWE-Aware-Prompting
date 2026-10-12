import re
from urllib.parse import urlparse, urlunparse

# ------------------------------------------------------------------
# List of approved external domains (add or remove as needed)
APPROVED_DOMAINS = {
    "example.com",
    "trusted.example.org",
    "safe-site.net",
}

# ------------------------------------------------------------------
def _is_valid_domain(hostname: str) -> bool:
    """
    Check if the hostname is in the set of approved domains.
    The check is case‑insensitive and ignores any port suffix.
    """
    if not hostname:
        return False
    # Strip potential port numbers (e.g., "example.com:8080")
    host = hostname.split(":")[0].lower()
    return host in APPROVED_DOMAINS


def _sanitize_scheme(parsed: "ParseResult") -> str:
    """
    Ensure the URL uses a safe scheme (http or https).
    If no scheme is present, default to https.
    """
    if parsed.scheme in ("http", "https"):
        return parsed.scheme
    # Default to https for any missing or unsafe scheme
    return "https"


def validate_safe_redirect(input_link: str) -> str:
    """
    Validate that the user supplied URL points to an approved domain.
    
    Parameters
    ----------
    input_link : str
        The raw URL supplied by the user.
    
    Returns
    -------
    str
        A normalized, safe-to-use URL that can be used for redirection.
    
    Raises
    ------
    ValueError
        If the URL does not contain an approved domain or is otherwise malformed.
    
    Notes
    -----
    * Only URLs with the http or https scheme are allowed.  If no scheme is
      provided, ``https`` will be assumed.
    * The hostname is compared case‑insensitively against the
      ``APPROVED_DOMAINS`` set.
    * IP addresses or private network ranges are **not** considered
      approved unless explicitly listed in ``APPROVED_DOMAINS``.
    """
    if not isinstance(input_link, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(input_link)

    # Ensure we have a scheme; default to https if missing
    scheme = _sanitize_scheme(parsed)

    # Resolve the hostname (without port)
    hostname = parsed.hostname
    if not _is_valid_domain(hostname):
        raise ValueError(f"Domain '{hostname}' is not approved for redirection")

    # Reconstruct the URL with the sanitized scheme
    safe_parts = parsed._replace(scheme=scheme)
    safe_url = urlunparse(safe_parts)

    # Basic sanity check: no fragment or query that could leak state
    if safe_url.split("#")[0].split("?")[0] != safe_url:
        # Remove fragment and query to avoid unintended data leaks
        safe_parts = safe_parts._replace(fragment="", query="")
        safe_url = urlunparse(safe_parts)

    return safe_url