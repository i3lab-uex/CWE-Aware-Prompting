import urllib.parse
from typing import List

# Predefined set of safe domains for redirection
ALLOWED_DOMAINS: List[str] = [
    "example.com",
    "trusted.org",
    "safe-site.net",
]

def _normalize_domain(domain: str) -> str:
    """
    Normalise a domain for comparison: lower‑case and strip leading/trailing dots.
    """
    return domain.lower().strip(" .")

def process_user_redirect(input_url: str) -> str:
    """
    Accept a user‑provided URL, validate that its domain is within the
    allowed list, and return a sanitized URL suitable for redirection.

    Parameters:
        input_url (str): The raw URL supplied by the user.

    Returns:
        str: A sanitized, safe URL that can be used for redirection.

    Raises:
        ValueError: If the input_url is not a valid URL or its domain
                    is not in ALLOWED_DOMAINS.
    """
    # Parse the URL and ensure it contains a scheme and network location
    parsed = urllib.parse.urlparse(input_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL: missing scheme or host")

    # Only allow http and https schemes
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Invalid URL: scheme must be http or https")

    # Normalise and compare the domain
    input_domain = _normalize_domain(parsed.netloc.split(":")[0])  # ignore port
    if input_domain not in {_normalize_domain(d) for d in ALLOWED_DOMAINS}:
        raise ValueError(f"Domain '{input_domain}' is not allowed")

    # Re‑construct the URL to ensure it contains only the essential components
    sanitized = urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,   # keep the host (and port if present)
        parsed.path or "/",  # default to root path
        "",              # params
        parsed.query,    # preserve query string if any
        ""               # fragment (strip to avoid navigation)
    ))
    return sanitized

# Example usage:
if __name__ == "__main__":
    try:
        url = process_user_redirect("https://example.com/welcome?ref=123")
        print(f"Safe redirect URL: {url}")
    except ValueError as e:
        print(f"Redirection blocked: {e}")