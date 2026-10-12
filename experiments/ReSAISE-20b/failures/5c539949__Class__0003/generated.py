import re
from urllib.parse import urlparse, ParseResult

# List of approved domains.  Add or remove entries as needed.
APPROVED_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "secure.example.net",
}

# Regular expression to validate that a domain is fully qualified
DOMAIN_REGEX = re.compile(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def _is_approved_domain(domain: str) -> bool:
    """
    Check whether the supplied domain is in the approved list.
    Subdomains are allowed if their parent domain is approved.

    :param domain: The hostname part of the URL.
    :return: True if the domain is approved, False otherwise.
    """
    # Normalize the domain
    domain = domain.lower().strip()

    if not DOMAIN_REGEX.match(domain):
        return False

    # Exact match
    if domain in APPROVED_DOMAINS:
        return True

    # Allow subdomains of approved domains
    for approved in APPROVED_DOMAINS:
        if domain.endswith("." + approved):
            return True

    return False


def secure_redirect_handler(redirect_url: str) -> str:
    """
    Validate a user-supplied URL against an approved domain list and return
    the URL if it is considered safe for redirection.

    This function does **not** act as a proxy or intermediary; it simply
    validates and returns the URL so that calling code can perform an
    actual redirect (e.g., via HTTP 302) without exposing the application
    to unintended proxying risks (CWE‑441).

    :param redirect_url: The URL supplied by the user.
    :return: The validated URL that is safe for redirection.
    :raises ValueError: If the domain is not approved or the URL is malformed.
    """
    if not isinstance(redirect_url, str):
        raise ValueError("Redirect URL must be a string")

    parsed: ParseResult = urlparse(redirect_url)

    # Reject relative URLs and unsupported schemes
    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only absolute HTTP/HTTPS URLs are allowed")

    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    # Ensure the domain is approved
    if not _is_approved_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not approved for redirection")

    # Reconstruct the URL to ensure canonical form
    safe_url = parsed.geturl()

    return safe_url