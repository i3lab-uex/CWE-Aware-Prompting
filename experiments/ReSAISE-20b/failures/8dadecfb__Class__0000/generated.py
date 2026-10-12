import re
from urllib.parse import urlparse, urlunparse

# List of domains that are allowed to be used for redirection.
APPROVED_DOMAINS = {
    "example.com",
    "myapp.com",
    "trusted.org",
}

# Regular expression to validate domain names.
_DOMAIN_REGEX = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+"
    r"[a-zA-Z]{2,}$"
)

def _is_valid_domain(domain: str) -> bool:
    """Return True if domain is syntactically valid and in the approved list."""
    # Strip port if present.
    host = domain.split(":")[0]
    return bool(_DOMAIN_REGEX.match(host)) and host.lower() in APPROVED_DOMAINS

def validate_redirect_url(input_url: str) -> str:
    """
    Validate a user supplied URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The URL supplied by the user.

    Returns
    -------
    str
        The fully qualified, validated URL safe for redirection.

    Raises
    ------
    ValueError
        If the input_url is not absolute or its domain is not approved.
    """
    # Parse the URL. If it has no scheme, treat as relative and reject.
    parsed = urlparse(input_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute and include a scheme (http/https).")

    # Normalize scheme to lower case.
    scheme = parsed.scheme.lower()
    if scheme not in ("http", "https"):
        raise ValueError("Only http and https schemes are allowed.")

    # Validate the domain.
    if not _is_valid_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not approved for redirection.")

    # Reconstruct the URL to avoid manipulation via fragments or query parameters
    safe_url = urlunparse((
        scheme,
        parsed.netloc.lower(),
        parsed.path or "/",
        "",  # params
        parsed.query,
        ""   # fragment
    ))
    return safe_url

# Example usage:
if __name__ == "__main__":
    try:
        url = validate_redirect_url("https://example.com/path?param=value")
        print(f"Safe redirect URL: {url}")
    except ValueError as exc:
        print(f"Invalid redirect: {exc}")