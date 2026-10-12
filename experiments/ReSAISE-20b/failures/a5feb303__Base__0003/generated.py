import re
from urllib.parse import urlparse, urlunparse

# List of domains that are considered safe for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trusted.org",
    "myapp.local",  # internal domain
}

# Regular expression to match valid domain names (RFC 1035)
DOMAIN_REGEX = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)$"
)


def _is_valid_domain(domain: str) -> bool:
    """
    Verify that the domain string is syntactically valid.
    """
    if not DOMAIN_REGEX.match(domain):
        return False
    # Reject IP addresses for this example
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain):
        return False
    return True


def process_user_redirect(input_url: str) -> str:
    """
    Sanitize a user supplied URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A fully qualified, safe URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the supplied URL is malformed or its domain is not in ALLOWED_DOMAINS.
    """
    if not input_url:
        raise ValueError("Empty URL provided")

    # Parse the URL
    parsed = urlparse(input_url)

    # Ensure we have a scheme and netloc; otherwise, treat as relative
    if not parsed.scheme or not parsed.netloc:
        # Reject relative URLs for security reasons
        raise ValueError("Relative URLs are not allowed")

    # Normalize the domain to lower case for comparison
    netloc = parsed.netloc.lower()

    # Strip port if present, e.g., example.com:8080 -> example.com
    domain = netloc.split(":")[0]

    # Validate the domain format
    if not _is_valid_domain(domain):
        raise ValueError(f"Invalid domain: {domain}")

    # Check against allowed domains
    if domain not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not allowed")

    # Rebuild the URL to ensure no unwanted components are present
    sanitized = urlunparse(
        (
            parsed.scheme,
            netloc,
            parsed.path or "/",
            "",  # params
            parsed.query,  # preserve query string if any
            "",  # fragment
        )
    )

    return sanitized