import re
from urllib.parse import urlparse, urlunparse

# List of domains that are considered safe for redirection
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.localhost",   # internal dev domain
}

# Regex to detect suspicious patterns (e.g., port numbers, IP addresses)
SUSPICIOUS_PATTERN = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$|:.*$")

def _is_approved(domain: str) -> bool:
    """
    Check if the given domain is in the approved list.
    """
    return domain.lower() in APPROVED_DOMAINS

def _sanitize_url(parsed: urlparse) -> str:
    """
    Reconstruct the URL ensuring that it does not contain any
    dangerous components such as port numbers or IP addresses.
    """
    # Remove fragment and query to avoid leaking sensitive data
    cleaned = parsed._replace(fragment="", query="")
    return urlunparse(cleaned)

def redirect_user_safely(target_url: str) -> str:
    """
    Validate a user-supplied URL and return it if it is safe for redirection.

    Parameters
    ----------
    target_url : str
        The URL input provided by the user.

    Returns
    -------
    str
        The validated, sanitized absolute URL ready for redirection.

    Raises
    ------
    ValueError
        If the URL's domain is not part of the approved list or if it contains
        suspicious patterns (e.g., IP addresses, port numbers).
    """
    # Parse the URL
    parsed = urlparse(target_url)

    # If scheme is missing, assume http and re-parse
    if not parsed.scheme:
        parsed = urlparse(f"http://{target_url}")

    # Ensure we have a network location
    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    # Reject URLs with IP addresses or port numbers
    if SUSPICIOUS_PATTERN.search(parsed.netloc):
        raise ValueError("URL contains an IP address or port number, which is not allowed")

    # Validate domain against approved list
    domain = parsed.hostname or ""
    if not _is_approved(domain):
        raise ValueError(f"Domain '{domain}' is not approved for redirection")

    # Return a sanitized version of the URL
    return _sanitize_url(parsed)