import re
from urllib.parse import urlparse, ParseResult

# List of domains that are allowed to be redirected to.
# You can add or remove entries as needed.
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "secure.example.net",
}

# Regular expression to validate that the URL uses a safe scheme.
SAFE_SCHEMES = re.compile(r"^(https?)://", re.IGNORECASE)


def _is_approved_domain(domain: str) -> bool:
    """
    Check whether a domain is in the approved list.
    Subdomains are allowed only if they match an entry exactly or
    end with a dot followed by an approved domain.
    """
    # Normalize the domain to lower case
    domain = domain.lower()

    if domain in APPROVED_DOMAINS:
        return True

    # Check for subdomains: e.g., foo.example.com
    for approved in APPROVED_DOMAINS:
        if domain.endswith("." + approved):
            return True

    return False


def redirect_user_safely(target_url: str) -> str:
    """
    Validate a user‑supplied URL and return it only if its domain
    is on the approved list.  Raises ValueError otherwise.

    Parameters:
        target_url (str): The URL supplied by the user.

    Returns:
        str: The validated, safe URL.

    Raises:
        ValueError: If the URL is malformed, uses an unsafe scheme,
                    or its domain is not approved.
    """
    # Basic syntax check
    if not target_url:
        raise ValueError("URL cannot be empty")

    # Ensure the URL starts with http:// or https://
    if not SAFE_SCHEMES.match(target_url):
        raise ValueError("Only HTTP and HTTPS URLs are allowed")

    # Parse the URL
    parsed: ParseResult = urlparse(target_url)

    if not parsed.netloc:
        raise ValueError("URL must contain a valid domain")

    # Validate the domain against the approved list
    if not _is_approved_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not approved for redirection")

    # Rebuild the URL to avoid any hidden characters or encoding issues
    safe_url = parsed.geturl()

    return safe_url