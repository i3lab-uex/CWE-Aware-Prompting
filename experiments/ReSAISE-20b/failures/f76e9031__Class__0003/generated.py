import re
from urllib.parse import urlparse

# List of domains that are allowed for redirection.
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "mycompany.net",
}

# Regular expression to validate a well‑formed domain name.
_DOMAIN_REGEX = re.compile(
    r"^(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a‑zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a‑zA-Z]{2,}$"
)


def _is_valid_domain(domain: str) -> bool:
    """Check that the domain is syntactically valid."""
    return bool(_DOMAIN_REGEX.match(domain))


def redirect_user_safely(target_url: str) -> str:
    """
    Validate a user‑supplied URL and return it only if its domain is in the
    approved list. Raises ValueError otherwise.

    Parameters
    ----------
    target_url : str
        The URL supplied by the user that should be redirected to.

    Returns
    -------
    str
        The original URL if it is safe for redirection.

    Raises
    ------
    ValueError
        If the URL has an unsupported scheme, a malformed domain, or its
        domain is not in APPROVED_DOMAINS.
    """
    if not isinstance(target_url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(target_url)

    # Scheme must be HTTP or HTTPS
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Unsupported URL scheme")

    # A netloc (domain) must be present
    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    # Normalise the host part (strip any port)
    host = parsed.hostname
    if not host or not _is_valid_domain(host):
        raise ValueError("Malformed domain name")

    # Check against the whitelist
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # All checks passed – return the original URL
    return target_url