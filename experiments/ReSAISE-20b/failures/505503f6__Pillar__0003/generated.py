import re
from urllib.parse import urlparse, urlunparse

# List of approved external domains (case‑insensitive)
APPROVED_DOMAINS = {
    "example.com",
    "trustedpartner.org",
    "safe-site.net",
}

# Regular expression to validate scheme
_SCHEME_RE = re.compile(r"^(https?)$", re.IGNORECASE)


def _canonical_domain(netloc: str) -> str:
    """
    Return the domain part of a netloc, lower‑cased and without port.
    """
    # Split host:port
    host = netloc.split(":")[0]
    return host.lower()


def validate_safe_redirect(input_link: str) -> str:
    """
    Validate that a user supplied URL is safe for redirection.

    Parameters
    ----------
    input_link : str
        The URL supplied by the user.

    Returns
    -------
    str
        A sanitized, safe‑to‑use URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL is not absolute, uses an unsupported scheme,
        or its domain is not in `APPROVED_DOMAINS`.
    """
    if not isinstance(input_link, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(input_link)

    # Reject relative URLs (no scheme or netloc)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute")

    # Validate scheme
    if not _SCHEME_RE.match(parsed.scheme):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Canonicalise domain
    domain = _canonical_domain(parsed.netloc)

    if domain not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved for redirection")

    # Re‑construct the URL to ensure no query or fragment leaks
    safe_parsed = parsed._replace(query="", fragment="")
    return urlunparse(safe_parsed)