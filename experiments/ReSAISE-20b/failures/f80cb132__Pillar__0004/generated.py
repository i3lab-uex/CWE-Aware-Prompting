import re
from urllib.parse import urlparse, urlunparse

# List of approved external domains (case‑insensitive)
APPROVED_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "secure.example.net",
}

# Regular expression to validate that the URL scheme is http or https
_SCHEME_RE = re.compile(r"^(https?)://", re.IGNORECASE)


def _is_approved_domain(domain: str) -> bool:
    """
    Check whether a domain is in the approved list.
    Subdomains are allowed only if explicitly listed.
    """
    # Normalize domain to lower case
    domain = domain.lower()
    return domain in APPROVED_DOMAINS


def secure_user_redirect(url_input: str) -> str:
    """
    Validate a user supplied URL and return a safe, fully‑qualified URL
    that can be used for redirection.

    Parameters
    ----------
    url_input : str
        The URL supplied by the user.

    Returns
    -------
    str
        A validated and safe URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, has an unsupported scheme,
        or its domain is not in ``APPROVED_DOMAINS``.
    """
    if not url_input:
        raise ValueError("URL must not be empty")

    # Parse the URL
    parsed = urlparse(url_input)

    # Ensure scheme is http or https
    if not _SCHEME_RE.match(parsed.scheme):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http and https are allowed.")

    # Ensure the netloc (domain) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    # Validate the domain against approved list
    if not _is_approved_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not approved for redirection")

    # Re‑build the URL to ensure no accidental fragments or query injection
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        parsed.query,  # allow query parameters (trusted context)
        ""   # fragment removed for security
    ))

    return safe_url