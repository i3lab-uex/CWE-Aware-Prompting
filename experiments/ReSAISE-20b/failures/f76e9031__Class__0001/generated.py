#!/usr/bin/env python3
"""
Secure user redirection helper.

The function `redirect_user_safely` validates a user‑supplied URL against an
approved list of domains and returns the sanitized URL if it is allowed.
Otherwise, a ValueError is raised.

This implementation mitigates CWE‑441 (Unintended Proxy or Intermediary)
by ensuring that only approved domains are returned and by never
forwarding the request to any external actor.
"""

from urllib.parse import urlparse, urlunparse
import re

# List of approved domains (exact match).  Adjust as needed.
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "safe-domain.net",
}

# Regular expression to validate domain names (basic RFC 1035 compliance)
_DOMAIN_RE = re.compile(r"^(?=.{1,253}$)([a-z0-9](?:[a‑z0‑9\-]{0,61}[a‑z0‑9])?\.)+[a‑z]{2,63}$", re.IGNORECASE)


def _is_valid_domain(domain: str) -> bool:
    """Check if a domain name is syntactically valid."""
    return bool(_DOMAIN_RE.match(domain))


def redirect_user_safely(target_url: str) -> str:
    """
    Validate and return a user‑supplied URL if its domain is approved.

    Parameters
    ----------
    target_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        The sanitized, absolute URL that can be safely used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsafe scheme, or its domain is not approved.
    """
    if not isinstance(target_url, str):
        raise ValueError("target_url must be a string")

    # Parse the URL
    parsed = urlparse(target_url)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure netloc (domain) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    # Normalise the domain (lowercase)
    domain = parsed.netloc.lower()

    # Validate domain syntax
    if not _is_valid_domain(domain):
        raise ValueError(f"Invalid domain format: {domain}")

    # Check against the approved list
    if domain not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved for redirection")

    # Reconstruct the URL to avoid issues with fragments or params
    safe_url = urlunparse((
        parsed.scheme,
        domain,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # discard fragment
    ))

    return safe_url


# Example usage (for demonstration only; remove or guard with `if __name__ == "__main__":` in production)
if __name__ == "__main__":
    test_urls = [
        "https://example.com/welcome?ref=123",
        "http://trustedsite.org/dashboard#section",
        "https://malicious.com/evil",
    ]

    for url in test_urls:
        try:
            print(f"Redirecting to: {redirect_user_safely(url)}")
        except ValueError as e:
            print(f"Blocked: {e}")