import re
from urllib.parse import urlparse, urlunparse

# Predefined set of safe domains for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "myapp.local"
}

# Regular expression to extract domain part from a hostname
_DOMAIN_RE = re.compile(r"^(?:www\.)?([a-zA-Z0-9.-]+)$")


def _is_allowed_domain(hostname: str) -> bool:
    """
    Check whether the given hostname is allowed.
    Subdomains are considered valid only if they end with one of
    the allowed domains and have a dot separator.
    """
    match = _DOMAIN_RE.match(hostname.lower())
    if not match:
        return False
    domain = match.group(1)

    # Exact match or subdomain match (e.g. sub.example.com)
    return any(
        domain == allowed or domain.endswith("." + allowed)
        for allowed in ALLOWED_DOMAINS
    )


def user_defined_redirect(redirect_url: str) -> str:
    """
    Accepts a URL input from the user and returns a sanitized URL
    that is safe for redirection.

    Parameters:
        redirect_url (str): The user-provided URL.

    Returns:
        str: A sanitized URL that is considered safe for redirection.

    Raises:
        ValueError: If the domain of the provided URL is not part
                    of the allowed domains.
    """
    if not redirect_url:
        raise ValueError("Redirect URL must not be empty")

    parsed = urlparse(redirect_url)

    # Ensure the URL has a scheme and network location
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL format")

    # Validate the hostname
    if not _is_allowed_domain(parsed.hostname or ""):
        raise ValueError(f"Domain '{parsed.hostname}' is not allowed for redirection")

    # Reconstruct the URL to ensure it doesn't contain any
    # suspicious components (e.g. userinfo, port)
    sanitized = urlunparse((
        parsed.scheme,
        parsed.hostname,           # exclude port
        parsed.path or "",
        "",                         # params
        parsed.query or "",
        ""                          # fragment
    ))

    return sanitized