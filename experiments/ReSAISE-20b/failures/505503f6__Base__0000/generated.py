import re
from urllib.parse import urlparse, urlunparse

# List of domains that are allowed for external redirects.
# You can add or remove entries as needed.
APPROVED_DOMAINS = {
    "example.com",
    "trustedpartner.org",
    "cdn.safe-site.net",
}

# Regular expression to validate that a domain is in the approved list
DOMAIN_REGEX = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a‑zA‑Z0‑9\-]{0,61}[a-zA-Z0-9])?\.)*"
    r"(?:[a-zA-Z]{2,})$",
    re.UNICODE
)


def _is_approved_domain(domain: str) -> bool:
    """
    Check if the given domain (or its parent domain) is in the approved list.
    Supports subdomains by walking up the domain hierarchy.
    """
    # Normalise: strip port, convert to lower case
    domain = domain.lower()
    parts = domain.split(":")[0].split(".")
    while parts:
        candidate = ".".join(parts)
        if candidate in APPROVED_DOMAINS:
            return True
        parts.pop(0)  # remove the leftmost label and try again
    return False


def validate_safe_redirect(input_link: str) -> str:
    """
    Validate a user-provided URL for safe redirection.

    Parameters
    ----------
    input_link : str
        The URL provided by the user.

    Returns
    -------
    str
        A sanitized, fully-qualified URL that is safe to use for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, has an unsupported scheme,
        or its domain is not in the approved list.
    """
    if not isinstance(input_link, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(input_link)

    # Scheme must be http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Netloc must contain a domain (and optionally port)
    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    # Validate the domain format
    if not DOMAIN_REGEX.match(parsed.netloc.split(":")[0]):
        raise ValueError(f"Invalid domain format: {parsed.netloc}")

    # Check if the domain is approved
    if not _is_approved_domain(parsed.netloc):
        raise ValueError(f"Domain not approved: {parsed.netloc}")

    # Reconstruct the URL to ensure it is fully-qualified and safe
    sanitized = urlunparse(parsed)

    return sanitized