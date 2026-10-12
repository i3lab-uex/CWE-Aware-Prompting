import re
from urllib.parse import urlparse, urlunparse

# Pre-approved domains for safe redirection (use punycode for IDNs if needed)
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "my-site.net",
}

# Regular expression to detect potentially malicious schemes or double slashes
INVALID_SCHEMES_RE = re.compile(r"^(javascript|data|vbscript):", re.IGNORECASE)

def secure_user_redirect(url_input: str) -> str:
    """
    Validate a user-provided URL and ensure it points to an approved domain.
    
    Parameters
    ----------
    url_input : str
        The URL supplied by the user.

    Returns
    -------
    str
        A fully-qualified, validated URL safe for redirection.

    Raises
    ------
    ValueError
        If the URL scheme is disallowed, if it contains an unsafe path,
        or if its domain is not in the approved list.
    """
    # Strip surrounding whitespace
    url_input = url_input.strip()
    
    # Reject empty input
    if not url_input:
        raise ValueError("Empty URL provided")

    # Reject dangerous schemes
    if INVALID_SCHEMES_RE.match(url_input):
        raise ValueError("Disallowed URL scheme")

    # Parse the URL
    parsed = urlparse(url_input)

    # Ensure we have a scheme and netloc; otherwise, treat as relative
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute and include a scheme")

    # Normalize the domain to lowercase for comparison
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Check that the domain is in the approved list
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Optional: enforce a specific scheme (e.g., https)
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only http and https schemes are allowed")

    # Ensure the path does not contain suspicious patterns (e.g., backslashes)
    if "\\" in parsed.path:
        raise ValueError("Backslash characters are not allowed in URL path")

    # Reconstruct the URL to ensure canonical form
    safe_url = urlunparse(parsed)

    return safe_url