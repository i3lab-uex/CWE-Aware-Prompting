import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (can be extended)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "safe-redirect.net",
}

# Optional: allow subdomains of approved domains
ALLOW_SUBDOMAINS = True

def _is_domain_approved(host: str) -> bool:
    """
    Check if the host is in the approved domain list.
    If ALLOW_SUBDOMAINS is True, any sub‑domain of an approved domain
    will also be considered valid.
    """
    host = host.lower()
    if host in APPROVED_DOMAINS:
        return True
    if ALLOW_SUBDOMAINS:
        for domain in APPROVED_DOMAINS:
            # match subdomains ending with .domain
            if host.endswith("." + domain):
                return True
    return False

def _sanitize_url(parsed: "ParseResult") -> str:
    """
    Rebuild the URL using only safe components.
    Strip any fragment and ensure scheme is http or https.
    """
    scheme = parsed.scheme.lower()
    if scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {scheme}")

    # Normalize netloc (remove default ports)
    netloc = parsed.netloc.lower()
    if scheme == "http" and netloc.endswith(":80"):
        netloc = netloc[:-3]
    if scheme == "https" and netloc.endswith(":443"):
        netloc = netloc[:-4]

    # Rebuild URL without fragment
    sanitized = urlunparse(
        (scheme, netloc, parsed.path or "/", parsed.params or "", parsed.query or "", "")
    )
    return sanitized

def handle_user_redirect(user_url: str) -> str:
    """
    Validate and sanitize a user supplied URL before redirecting.

    Parameters
    ----------
    user_url : str
        The raw URL entered by the user.

    Returns
    -------
    str
        A sanitized, approved URL suitable for redirecting.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        or its domain is not in the approved list.
    """
    if not user_url:
        raise ValueError("URL must not be empty")

    # Parse the URL
    parsed = urlparse(user_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include a scheme and host")

    # Validate domain
    if not _is_domain_approved(parsed.hostname or ""):
        raise ValueError(f"Domain '{parsed.hostname}' is not approved for redirection")

    # Sanitize and return
    return _sanitize_url(parsed)