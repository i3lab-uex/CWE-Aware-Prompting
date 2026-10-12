import re
from urllib.parse import urlparse, urlunparse, ParseResult

# Define the set of domains that are considered safe for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "myapp.local"
}

# Regular expression to validate that a domain is an allowed domain or its subdomain
DOMAIN_PATTERN = re.compile(rf"^(?:[\w-]+\.)*({'|'.join(map(re.escape, ALLOWED_DOMAINS))})$")

def process_user_redirect(input_url: str) -> str:
    """
    Sanitize and validate a user-provided URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A sanitized, fully-qualified URL that is safe to redirect to.

    Raises
    ------
    ValueError
        If the URL's domain is not in ALLOWED_DOMAINS.
    """
    if not isinstance(input_url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(input_url)

    # Ensure that a scheme and netloc are present; otherwise, assume relative URL
    if not parsed.scheme or not parsed.netloc:
        # Treat as a path-only redirect (e.g., "/home")
        sanitized = urlunparse(ParseResult(scheme="", netloc="", path=parsed.path,
                                           params="", query=parsed.query, fragment=""))
        return sanitized

    # Validate the domain
    domain = parsed.hostname or ""
    if not DOMAIN_PATTERN.match(domain.lower()):
        raise ValueError(f"Domain '{domain}' is not allowed for redirection")

    # Reconstruct the URL to avoid any malicious fragments or unusual schemes
    safe_parsed = ParseResult(
        scheme=parsed.scheme.lower(),
        netloc=domain,
        path=parsed.path,
        params="",
        query=parsed.query,
        fragment=""
    )
    return urlunparse(safe_parsed)