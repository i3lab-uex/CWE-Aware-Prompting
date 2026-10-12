import re
from urllib.parse import urlparse

# List of approved domains (exact match or subdomain allowed)
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "safe-site.net",
}

# Regular expression to validate a well‑formed URL
URL_REGEX = re.compile(
    r"^(https?://)"          # scheme
    r"(?:(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,})"  # domain
    r"(?:/[^?#]*)?"          # path
    r"(?:\?[^#]*)?"          # query
    r"(?:#[^\s]*)?$",        # fragment
    re.IGNORECASE,
)


def _is_approved_domain(domain: str) -> bool:
    """
    Return True if `domain` is exactly in the approved list or a sub‑domain
    of an approved domain.
    """
    # Normalize to lower case and strip trailing dot
    domain = domain.lower().rstrip(".")
    if domain in APPROVED_DOMAINS:
        return True

    # Check sub‑domain
    for approved in APPROVED_DOMAINS:
        if domain.endswith("." + approved):
            return True
    return False


def secure_redirect_handler(redirect_url: str) -> str:
    """
    Validate a user‑supplied URL and return it only if its domain is in the
    approved list.  Raises ValueError otherwise.

    Args:
        redirect_url: The URL supplied by the user.

    Returns:
        The validated, safe URL string.
    """
    if not redirect_url or not isinstance(redirect_url, str):
        raise ValueError("Redirect URL must be a non‑empty string")

    # Basic syntactic validation
    if not URL_REGEX.match(redirect_url):
        raise ValueError("Malformed URL")

    parsed = urlparse(redirect_url)

    # Ensure scheme is HTTP/HTTPS
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError("Only HTTP and HTTPS URLs are allowed")

    # Validate domain
    if not _is_approved_domain(parsed.hostname or ""):
        raise ValueError(f"Domain '{parsed.hostname}' is not approved for redirects")

    # Re‑construct the URL to avoid any hidden components
    safe_url = parsed.geturl()
    return safe_url


# Example usage (for testing only; remove or guard with __name__ == "__main__" in production)
if __name__ == "__main__":
    try:
        print(secure_redirect_handler("https://sub.example.com/path?query=1"))
    except ValueError as exc:
        print(f"Redirect rejected: {exc}")