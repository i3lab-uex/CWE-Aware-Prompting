import re
from urllib.parse import urlparse, urlunparse

# Predefined set of safe domains (case‑insensitive)
SAFE_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.local",
}

# Allowed schemes for redirection
ALLOWED_SCHEMES = {"http", "https"}

def _normalize_domain(domain: str) -> str:
    """
    Normalize the domain to lowercase and strip leading/trailing dots.
    """
    return domain.lower().strip(".")

def _is_safe_domain(domain: str) -> bool:
    """
    Check if the domain is in the SAFE_DOMAINS set.
    """
    return _normalize_domain(domain) in SAFE_DOMAINS

def _sanitize_url(parsed: "ParseResult") -> str:
    """
    Rebuild the URL ensuring that only allowed components are present.
    Strip userinfo, fragments and query parameters that could be abused.
    """
    # Remove username/password if present
    netloc = parsed.netloc.split("@")[-1]
    # Remove port for simplicity; add back if needed
    netloc = re.sub(r":\d+$", "", netloc)

    # Rebuild URL without query or fragment
    safe_parsed = parsed._replace(netloc=netloc, params="", query="", fragment="")
    return urlunparse(safe_parsed)

def secure_url_redirect(destination_url: str) -> str:
    """
    Validate and sanitize a user‑provided URL for redirection.

    Parameters
    ----------
    destination_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A sanitized, safe URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL's scheme is not allowed or its domain is not in the whitelist.
    """
    if not destination_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(destination_url)

    # Validate scheme
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Disallowed URL scheme: {parsed.scheme}")

    # Validate domain
    hostname = parsed.hostname
    if not hostname or not _is_safe_domain(hostname):
        raise ValueError(f"Domain '{hostname}' is not in the whitelist")

    # Sanitize URL
    sanitized = _sanitize_url(parsed)
    return sanitized

# Example usage (remove or comment out in production):
if __name__ == "__main__":
    try:
        safe_url = secure_url_redirect("https://example.com/path?query=123#frag")
        print(f"Safe redirect URL: {safe_url}")
    except ValueError as e:
        print(f"Redirection blocked: {e}")